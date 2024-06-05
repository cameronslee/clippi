import os
import sys
import shutil
import pandas as pd
from tqdm import tqdm
from pydub import AudioSegment

### === Helpers === ###
def perror(msg):
    print("error: " + msg)

def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    print("path already exists")
    return

def mp3_to_wav(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format="wav")

def split_audio(input_file, output_dir, duration_ms):
    audio = AudioSegment.from_wav(input_file)
    num_clips = len(audio) // duration_ms

    for i in range(num_clips):
        start_time = i * duration_ms
        end_time = (i + 1) * duration_ms
        clip = audio[start_time:end_time]

        #build output file path from output_dir + input file
        output_file = os.path.join(output_dir, f"{os.path.splitext(input_file)[0].rsplit('/', 1)[-1]}_clip_{i+1}.wav")
        clip.export(output_file, format="wav")

usage_string = """
usage: text_preprocessing <filename>              perform preprocessing
"""
def usage():
    print(usage_string)

# Transcript
INPUT_DIR = './input_data/'

# Driver
def main():
    if (len(sys.argv)) < 2:
        usage()
        exit(1)

    INPUT_FILE = sys.argv[1]
    root, extension  = os.path.splitext(INPUT_FILE)
    OUTPUT_DIR = './cache/' + root + '/' # target output for preoprocessing is cache
    OUTPUT_FILE = OUTPUT_DIR + root + ".wav"
    CLIPS_DIR = OUTPUT_DIR + root + '_clips/'
    mkdir(OUTPUT_DIR)   # create subdirectory in cache

    print("Processing: " + INPUT_FILE)

    if not os.path.isfile(INPUT_DIR + INPUT_FILE):  # specified file not found
        perror("unable to process input file " + str(INPUT_FILE))
        exit(1)

    # if mp3, check cache and convert to wav if needed
    if extension != '.wav' and not os.path.isfile(OUTPUT_FILE):
        print(f"converting {INPUT_FILE} to .wav ...")
        try:
            mp3_to_wav(INPUT_DIR + INPUT_FILE, OUTPUT_FILE)
        except:
            perror(f"unable to convert input file '{INPUT_FILE}' to .wav")
            #exit(1)

    if os.path.isdir(CLIPS_DIR): # clear prev clips
        shutil.rmtree(CLIPS_DIR)

    mkdir(CLIPS_DIR)
    split_audio(OUTPUT_FILE, CLIPS_DIR, 3000)   # specify clip length in ms

    # try:
    #     # TODO find appropriate model for audio classification
    #     # process data, place into dataframe with beginning and end timestamps, audio appropriate labels

    # except:
    #     perror("unable to create dataset")
    #     exit(1)

    # Export
    #df.to_csv(OUTPUT_DIR + root + '_out_text_preprocessing.csv', index=False) 

if __name__ == "__main__":
    main()