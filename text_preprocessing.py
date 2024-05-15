import json
from tqdm import tqdm
from helpers import perror

### === Transcript === ###
import whisper_timestamped as whisper
def get_transcript(input_file, output_file):
    audio = whisper.load_audio(input_file)
    model = whisper.load_model("base")

    result = whisper.transcribe(model, audio, language="en")

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    return result

### === Dataframe === ###
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

### === Sentiment Analysis === ###
from transformers import pipeline
# Model: [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions) 
#        [ONNX Variant](https://huggingface.co/SamLowe/roberta-base-go_emotions-onnx)
#
# Model trained from [roberta-base](https://huggingface.co/roberta-base) on the
# [go_emotions](https://huggingface.co/datasets/go_emotions) dataset for multi-label classification.
sentiment_pipe = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def get_sentiment(row):
    return sentiment_pipe(row['text'])[0] # produces a list of dicts for each label

def unpack_sentiment(row):
    sentiment = row['sentiment']
    if sentiment:
        for label_dict in sentiment:
            label = label_dict['label'] + "_sentiment"
            score = label_dict['score']
            row[label] = score
    return row

positive_labels = [
    'admiration_sentiment',
    'amusement_sentiment',
    'approval_sentiment',
    'caring_sentiment',
    'curiosity_sentiment',
    'desire_sentiment',
    'gratitude_sentiment',
    'joy_sentiment',
    'love_sentiment',
    'optimism_sentiment',
    'pride_sentiment',
    'relief_sentiment',
    'surprise_sentiment',
]

def get_positive_sentiment(row):
    res = 0
    for label in positive_labels:
        res += row[label]

    return res

negative_labels = [
    'anger_sentiment',
    'annoyance_sentiment',
    'confusion_sentiment',
    'disappointment_sentiment',
    'disapproval_sentiment',
    'disgust_sentiment',
    'embarrassment_sentiment',
    'grief_sentiment',
    'nervousness_sentiment',
    'realization_sentiment',
    'remorse_sentiment',
    'sadness_sentiment',
]

def get_negative_sentiment(row):
    res = 0
    for label in negative_labels:
        res += row[label]

    return res

### === Entity Recognition === ###
import spacy
def get_entity_values(row):
    doc = nlp(row['text'])
    # Extract entity details and return as a list of tuples
    return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
# Run this:
# $ python3 -m spacy download en
nlp = spacy.load("en_core_web_sm")
#nlp = spacy.load("en_core_web_lg")

### === Driver === ###
import os

PREPROCESSING_OUTPUT_DIR = "./cache/"

def preprocess_text(input_file, output_file, output_dir):
    print("text_preprocessing: processing" + input_file)
    # Generate transcript if it does not exist in cache
    if not os.path.isfile(output_file):
        try:
            transcript_out = os.path.basename(input_file) + "_transcript"
            transcript = get_transcript(input_file, PREPROCESSING_OUTPUT_DIR + transcript_out) 
        except:
            perror("unable to generate transcript")
    else: 
        try:
            with open(output_file, 'r') as f:
                transcript = f.read()
                transcript = json.loads(transcript)
        except:
            perror("unable to load data from cache")

    try:
        df = pd.DataFrame(transcript)
    except:
        perror("unable to create dataset")
        exit(1)

    try:
        tqdm.pandas(desc="processing text data")
        df['text'] = df.progress_apply(get_text,axis=1)
        df['text_len'] = df.progress_apply(get_length,axis=1)
        df['start'] = df.progress_apply(get_start,axis=1)
        df['end'] = df.progress_apply(get_end,axis=1)
        df['duration'] = df.progress_apply(get_duration,axis=1)
    except:
        perror("unable to process text data")
        exit(1)

    try:
        tqdm.pandas(desc="measuring sentiment")
        df['sentiment'] = df.progress_apply(get_sentiment, axis=1)
        df = df.apply(unpack_sentiment, axis=1)
        df['positive_sentiment'] = df.apply(get_positive_sentiment, axis=1)
        df['negative_sentiment'] = df.apply(get_negative_sentiment, axis=1)
    except:
        perror("unable measure sentiment")
        exit(1)

    try:
        tqdm.pandas(desc="searching for entities")
        df['entities'] = df.progress_apply(get_entity_values, axis=1)

    except:
        perror("unable to find entities")
        exit(1) 

    # Drop unncessary data
    df = df.drop(columns='language')
    df = df.drop(columns='segments')
    df = df.drop(columns='sentiment')

    # rename for consistency
    df = df.rename(columns={"start": "start_time", "end": "end_time"})

    # Export
    df.to_csv(output_dir + output_file, index=False) 
    
    print("text preprocessing complete")
