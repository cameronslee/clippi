import os
import sys
import shutil
import pandas as pd
import numpy as np

from tqdm import tqdm
from pydub import AudioSegment
from helpers import perror
from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

def mp3_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.set_frame_rate(16000)
    audio.export(output_file, format="wav")

usage_string = """
usage: text_preprocessing <filename>              perform preprocessing
"""
def usage():
    print(usage_string)

# Driver
def preprocess_audio(input_file, output_file, output_dir):
    basename, extension = os.path.splitext( os.path.basename(input_file))
    print("Audio preprocessing: " + input_file + "...")

    # convert to wav, place in cache
    if not os.path.isfile(output_dir + basename + '.wav'):
        try:
            mp3_to_wav(input_file, output_dir + basename + '.wav')
        except:
            perror(f"unable to convert input file '{input_file}' to .wav")
            exit(1)
            
    df = pd.DataFrame()

    # Customize and associate model for Classifier
    base_options = python.BaseOptions(model_asset_path='./clippi/classifier.tflite')
    options = audio.AudioClassifierOptions(
        base_options=base_options, max_results=4)

    # create classifier, segment audio clips, and classify
    with audio.AudioClassifier.create_from_options(options) as classifier:
        sample_rate, wav_data = wavfile.read(output_dir + basename + '.wav')
        audio_clip = containers.AudioData.create_from_array(
            wav_data.astype(float) / np.iinfo(np.int16).max, sample_rate)
        classification_result_list = classifier.classify(audio_clip)

        total_duration_ms = int(((len(wav_data) / sample_rate) * 1000))
        timestamps = [i for i in range(0, total_duration_ms, 975)]

        # insert clips into dataframe
        for idx, timestamp in enumerate(timestamps):
            classification_result = classification_result_list[idx]
            top_category = classification_result.classifications[0].categories[0]
            df = df._append({
                'start_time': round(timestamp / 1000, 2),
                'end_time': round((timestamp + 975) / 1000, 2),
                'classification': top_category.category_name,
                'confidence': round(top_category.score, 2),  
            }, ignore_index=True)

        df.to_csv(output_dir + output_file, columns=['start_time', 'end_time', 'classification', 'confidence'], index=True)