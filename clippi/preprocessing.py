from text_preprocessing import preprocess_text
from vision_preprocessing import preprocess_vision
from audio_preprocessing import preprocess_audio
import pandas as pd
from helpers import perror
import os

def preprocess_all(input_file, text_output_file, audio_output_file, vision_output_file, output_dir):
    if not os.path.isfile(output_dir+text_output_file):
        preprocess_text(input_file=input_file, output_file=text_output_file, output_dir=output_dir)
    else:
        print("found " + text_output_file + " in cache. loading...")
    if not os.path.isfile(output_dir+audio_output_file):
        preprocess_audio(input_file=input_file, output_file=audio_output_file, output_dir=output_dir)
    else:
        print("found " + audio_output_file + " in cache. loading...")
    if not os.path.isfile(output_dir+vision_output_file):
        preprocess_vision(input_file=input_file, output_file=vision_output_file, output_dir=output_dir)
    else:
        print("found " + vision_output_file + " in cache. loading...")

    try:
        df_text = pd.read_csv(output_dir+text_output_file)
        df_vision = pd.read_csv(output_dir+vision_output_file)
    except:
        perror("unable to load preprocessed CSV")
        exit(1)

    df = pd.concat([df_text, df_vision])

    print(df.info)

    df.set_index('start_time', inplace=True)
    df.sort_index(inplace=True)

    # FIXME pandas deprecated function
    df.fillna(method='bfill', inplace=True)

    df.to_csv(output_dir + "out_preprocessing.csv", index=True) 
    print("preprocessing complete")
