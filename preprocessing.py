import sys
import os
import ast
import pandas as pd
from collections import Counter

INPUT_DATA = "./input_data/"
OUTPUT_DATA = "./output_data/"
STAGED_DATA = "./staged_data/"

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    print("path already exists")
    return

def setup_preprocessing():
    mkdir(INPUT_DATA)
    mkdir(OUTPUT_DATA)
    mkdir(STAGED_DATA)

    print("preprocessing: setup complete")

def read_transcript(path):
    f = open(path, "r") 

    data = f.readlines()

    f.close()

    res = []
    for d in data:
        temp = ast.literal_eval(d)
        res.append(temp)

    return res

def get_length(row):
    return len(row['text'])

def to_dataframe(transcript):
    df = pd.DataFrame(transcript)
    df['text_len'] = df.apply(get_length,axis=1)

    return df

def preprocess(path_to_input_data):
    test_path = "./transcripts/JN3KPFbWCy8"


    transcript = read_transcript(path_to_input_data)

    df = to_dataframe(transcript)


    return df

### ========== NLP ========== ###
label_lookup_table = {
    "PERSON": "People, including fictional",
    "NORP": "Nationalities or religious or political groups",
    "FACILITY": "Buildings, airports, highways, bridges, etc.",
    "ORGANIZATION": "Companies, agencies, institutions, etc.",
    "GPE": "Countries, cities, states",
    "LOCATION": "Non-GPE locations, mountain ranges, bodies of water",
    "PRODUCT": "Vehicles, weapons, foods, etc. (Not services)",
    "EVENT": "Named hurricanes, battles, wars, sports events, etc.",
    "WORK OF ART": "Titles of books, songs, etc.",
    "LAW": "Named documents made into laws",
    "LANGUAGE": "Any named language",
    "DATE": "Absolute or relative dates or periods",
    "TIME": "Times smaller than a day",
    "PERCENT": "Percentage (including “%”)",
    "MONEY": "Monetary values, including unit",
    "QUANTITY": "Measurements, as of weight or distance",
    "ORDINAL": "“first”, “second”",
    "CARDINAL": "Numerals that do not fall under another type"
}

# TODO prefetch this
import spacy
def ner(src):
    return spacy.load(src)

### ========== DRIVER ========== ###
def main():
    setup_preprocessing()
    df = preprocess(sys.argv[1])

    # Run this:
    # $ python3 -m spacy download en
    nlp = ner("en_core_web_lg")

    def get_entity_values(data):
        doc = nlp(data['text'])
        # Extract entity details and return as a list of tuples
        return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

    # assign entities
    df['entities'] = df.apply(get_entity_values, axis=1)

    # drop all with no entities
    df = df[df['entities'].str.len() > 0]

    def calculate_similarity(text1, text2):
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        return doc1.similarity(doc2)

    # Calculate similarity
    # Shift the 'text' column to align each row with its next neighbor for comparison
    df['next_text'] = df['text'].shift(-1)

    # Calculate similarity (dropping the last row to avoid comparing with NaN)
    df['similarity'] = df.iloc[:-1].apply(lambda row: calculate_similarity(row['text'], row['next_text']), axis=1)

    # Drop the 'next_text' column if no longer needed
    df.drop(columns=['next_text'], inplace=True)

    # Merge on similarity
    # hyperparam
    SIMILARITY_LOWER_BOUND = 0.3

    df['end'] = df['start'] + df['duration']

    # Identify rows to merge based on condition
    # Marking rows that should merge
    # Condition: similarity to next >= <SIMILARITY_LOWER_BOUND>
    df['merge_with_next'] = df['similarity'] >= SIMILARITY_LOWER_BOUND

    # group identifier
    df['group'] = (df['merge_with_next'] == False).cumsum()

    # merge rows within the same group
    aggregated = df.groupby('group').agg({
        'text': ' '.join, 
        'start': 'min',  # earliest start time
        'end': 'max',  # latest end time
        'entities': lambda x: sum(x, []),  # Concatenate all lists in group
    }).reset_index(drop=True)

    # calculate new duration
    aggregated['duration'] = aggregated['end'] - aggregated['start']

    df = aggregated

    # Target top three entities
    def extract_top_three_entities(entities):
        # Count occurrences 
        entity_counts = Counter(entity[0] for entity in entities)
        
        # top three based on occurrence
        top_three_entities = entity_counts.most_common(3)
        
        # extract entity names 
        top_three_entity_names = [entity[0] for entity in top_three_entities]
        
        return top_three_entity_names

    # Apply to df
    df['top_three_entities'] = df['entities'].apply(extract_top_three_entities)

    extracted_id = sys.argv[1].split("/")[-1]
    filename = OUTPUT_DATA+extracted_id+".csv"
    df.to_csv(filename, index=False)
    assert os.path.isfile(filename), "error: could not save preprocess data" 

    return

if __name__ == "__main__":
    main()

