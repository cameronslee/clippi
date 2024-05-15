import os
import sys
import pandas as pd
from tqdm import tqdm
import av
import numpy as np

from helpers import perror, mkdir

### === Sampling === ###
def read_video_pyav(container, indices):
    '''
    Decode the video with PyAV decoder.
    Args:
        container (`av.container.input.InputContainer`): PyAV container.
        indices (`List[int]`): List of frame indices to decode.
    Returns:
        result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
    '''
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)

    return np.stack([x.to_ndarray(format="rgb24") for x in frames])

def sample_frame_indices(clip_len, frame_sample_rate, seg_len, end_idx):
    '''
    Sample a given number of frame indices from the video.
    Args:
        clip_len (`int`): Total number of frames to sample.
        frame_sample_rate (`int`): Sample every n-th frame.
        seg_len (`int`): Maximum allowed index of sample's last frame. 
        end_idx (`int`): Last index considered

    Returns:
        indices (`List[int]`): List of sampled frame indices
    '''
    converted_len = int(clip_len * frame_sample_rate)
    start_idx = end_idx - converted_len
    indices = np.linspace(start_idx, end_idx, num=clip_len)
    indices = np.clip(indices, start_idx, end_idx - 1).astype(np.int64)

    return indices

### === VideoReader === ###
# decord notes:
# https://github.com/dmlc/decord?tab=readme-ov-file            aarch64: build from source to avoid shambles
# $ cd decord/python && pip install .                          
from decord import VideoReader, cpu

### === Model === ###
from transformers import AutoProcessor, AutoModel
processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")
video_labels = [
    "Highlight Worthy",
    "Neutral",
    "Not Highlight Worthy",
]

### === Inference === ###
import torch
# TODO perf bottleneck right here, batch this with torch dataset loader or something
def get_classification(row):
    video = np.array(row['video']) # perf improvement 
    inputs = processor(text=video_labels, videos=list(video), return_tensors="pt", padding=True)
    # forward pass
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = outputs.logits_per_video.softmax(dim=1)
    _, predicted = torch.max(probs, dim=1)

    return video_labels[predicted.item()]

### === Dataframe === ###
df = pd.DataFrame(columns=['start_frame', 'end_frame', 'start_time', 'end_time'])

### === Driver === ###
def preprocess_vision(input_file, output_file, output_dir):
    if not os.path.isfile(input_file):
        perror("unable to process input file " + str(input_file))
        exit(1)
    
    print("Processing: " + input_file)
    global df
    try:
        videoreader = VideoReader(uri=input_file, num_threads=1, ctx=cpu(0))
        container = av.open(input_file)
        SEGMENT_LENGTH = container.streams.video[0].frames
    except:
        perror("videoreader and container could not be initialized")

    if SEGMENT_LENGTH <= 0:
        perror("segment length must be greater than 0")
        exit(1)
    
    # frame sample size
    SAMPLE_SIZE = 8
    FRAME_SAMPLE_RATE = 1

    # Set up frame indicies
    avg_fps = videoreader.get_avg_fps()
    try:
        for i in range(0, (SEGMENT_LENGTH // SAMPLE_SIZE)):
            start_frame = i * SAMPLE_SIZE
            end_frame = (i * SAMPLE_SIZE) + SAMPLE_SIZE
            start_time = round(start_frame / avg_fps, 2)
            end_time = round(end_frame / avg_fps, 2)
            df.loc[len(df)] = [start_frame, end_frame, start_time, end_time]
        # Account for any clipping
        last_value = df['end_frame'].iloc[-1]
        df.loc[len(df)] = [last_value, SEGMENT_LENGTH-1, round(last_value / avg_fps), round(SEGMENT_LENGTH-1 / avg_fps)]
    except:
        perror("unable to initialize frame indices")
        exit(1)

    tqdm.pandas(desc="Processing Visual Data")
    def get_video(row):
        return videoreader.get_batch(sample_frame_indices(clip_len=SAMPLE_SIZE, frame_sample_rate=FRAME_SAMPLE_RATE, seg_len=container.streams.video[0].frames, end_idx=row['end_frame'])).asnumpy()
    try:
        df['video'] = df.progress_apply(get_video, axis=1)
    except:
        perror("unable to process visual data")
        exit(1)

    tqdm.pandas(desc="Running Inference")
    try:
        df['vision_classification'] = df.progress_apply(get_classification, axis=1)
    except:
        perror('unable to complete inference')
        exit(1)

    # drop video because its huge
    df = df.drop(columns=['video'])

    # export
    df.to_csv(output_dir + output_file, index=False) 

    print("vision preprocessing complete")