import os
import sys
import pandas as pd
from tqdm import tqdm
import av
import numpy as np

from helpers import perror, mkdir

### === Helpers === ###
import os
def perror(msg):
    print("error: " + msg)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    print("path already exists")
    return

OUTPUT_DIR = './cache/'  # target output for preoprocessing is cache

usage_string = """
usage: vision_preprocessing <filename>              perform preprocessing
"""
def usage():
    print(usage_string)

### === Dataframe === ###
df = pd.DataFrame(columns=['start_frame', 'end_frame', 'start_time', 'end_time'])

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

### === Driver === ###
def main():
    if (len(sys.argv)) < 2:
        usage()
        exit(1)
    
    INPUT_FILE = sys.argv[1]

    if not os.path.isfile(INPUT_FILE):
        perror("unable to process input file " + str(INPUT_FILE))
        exit(1)
    
    print("Processing: " + INPUT_FILE)
    global df
    videoreader = VideoReader(uri=INPUT_FILE, num_threads=1, ctx=cpu(0))
    container = av.open(INPUT_FILE)
    SEGMENT_LENGTH = container.streams.video[0].frames

    if SEGMENT_LENGTH <= 0:
        perror("video container could not be initialized")
        exit(1)
    
    # frame sample size
    SAMPLE_SIZE = 8
    FRAME_SAMPLE_RATE = 1

    # Set up frame indicies
    avg_fps = videoreader.get_avg_fps()
    for i in range(0, (SEGMENT_LENGTH // SAMPLE_SIZE)):
        start_frame = i * SAMPLE_SIZE
        end_frame = (i * SAMPLE_SIZE) + SAMPLE_SIZE
        start_time = round(start_frame / avg_fps, 2)
        end_time = round(end_frame / avg_fps, 2)
        df.loc[len(df)] = [start_frame, end_frame, start_time, end_time]

    # Account for any clipping
    last_value = df['end_frame'].iloc[-1]
    df.loc[len(df)] = [last_value, SEGMENT_LENGTH-1, round(last_value / avg_fps), round(SEGMENT_LENGTH-1 / avg_fps)]

    tqdm.pandas(desc="Processing Visual Data")
    # Get video
    def get_video(row):
        return videoreader.get_batch(sample_frame_indices(clip_len=SAMPLE_SIZE, frame_sample_rate=FRAME_SAMPLE_RATE, seg_len=container.streams.video[0].frames, end_idx=row['end_frame'])).asnumpy()
    df['video'] = df.progress_apply(get_video, axis=1)

    tqdm.pandas(desc="Running Inference")
    df['vision_classification'] = df.progress_apply(get_classification, axis=1)

    # Drop video because its huge
    df = df.drop(columns=['video'])

    # Export
    df.to_csv(OUTPUT_DIR + 'out_vision_preprocessing.csv', index=False) 

    print("vision preprocessing complete")
    
if __name__ == "__main__":
    main()  