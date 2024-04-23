import os
import sys
import whisper_timestamped as whisper # for transcript
import json
import pandas as pd
from tqdm import tqdm

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

usage_string = """
usage: text_preprocessing <filename>              perform preprocessing
"""
def usage():
    print(usage_string)

# Transcript
INPUT_FILE = "test1.mp4"
INPUT_DIR = './input_data'
OUTPUT_DIR = './cache/' # target output for preoprocessing is cache

root, extention  = os.path.splitext(INPUT_FILE)
OUTPUT_FILE = OUTPUT_DIR + root + ".json"

def get_transcript(input_file, output_file):
    audio = whisper.load_audio(input_file)
    model = whisper.load_model("base")

    result = whisper.transcribe(model, audio, language="en")

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    return result

# Dataframe
import pandas as pd
def get_text(row):
    return row['segments']['text']

def get_length(row):
    return len(row['segments']['text'])

def get_start(row):
    return row['segments']['start']

def get_end(row):
    return row['segments']['end']

def get_duration(row):
    return round(abs(row['segments']['end'] - row['segments']['start']), 2)

# Sentiment
from transformers import pipeline
# Model: [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions) 
#        [ONNX Variant](https://huggingface.co/SamLowe/roberta-base-go_emotions-onnx)
#
# Model trained from [roberta-base](https://huggingface.co/roberta-base) on the
# [go_emotions](https://huggingface.co/datasets/go_emotions) dataset for multi-label classification.
sentiment_pipe = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def get_sentiment(row):
    return sentiment_pipe(row['text'])[0] # produces a list of dicts for each label

# Entity Recognition
import spacy
# TODO design decision: handling empty columns, keep or toss
def get_entity_values(row):
    doc = nlp(row['text'])
    # Extract entity details and return as a list of tuples
    return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

# Run this:
# $ python3 -m spacy download en
#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_lg")

# Driver
def main():
    mkdir(OUTPUT_DIR) # TODO move this to main driver (clippy.py), should always be setup first
    if (len(sys.argv)) < 2:
        usage()
        exit(1)

    INPUT_FILE = sys.argv[1]
    print("Processing: " + INPUT_FILE)

    if not os.path.isfile(INPUT_FILE):
        perror("unable to process input file " + str(INPUT_FILE))
        exit(1)

    # Generate transcript if it does not exist in cache
    if not os.path.isfile(OUTPUT_FILE):
        try:
            transcript = get_transcript(INPUT_FILE, OUTPUT_FILE)
        except:
            perror("unable to generate transcript")
    else: 
        try:
            with open(OUTPUT_FILE, 'r') as f:
                transcript = f.read()
                transcript = json.loads(transcript)
        except:
            perror("unable to load data from cache")

    try:
        df = pd.DataFrame(transcript)
        tqdm.pandas(desc="Processing Text Data")
        df['text'] = df.progress_apply(get_text,axis=1)
        df['text_len'] = df.apply(get_length,axis=1)
        df['start'] = df.apply(get_start,axis=1)
        df['end'] = df.apply(get_end,axis=1)
        df['duration'] = df.apply(get_duration,axis=1)
        tqdm.pandas(desc="Measuring Sentiment")
        df['sentiment'] = df.progress_apply(get_sentiment, axis=1)
        tqdm.pandas(desc="Searching for Entities")
        df['entities'] = df.progress_apply(get_entity_values, axis=1)
        # Drop unncessary data
        df = df.drop(columns='language')
        df = df.drop(columns='segments')
    except:
        perror("unable to create dataset")
        exit(1)

    # Export
    df.to_csv(OUTPUT_DIR + 'out_text_preprocessing.csv', index=False) 
                                
if __name__ == "__main__":
    main()