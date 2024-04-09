import sys
import os
import ast
import pandas as pd

INPUT_DATA = "./input_data/"
OUTPUT_DATA = "./output_data/"
STAGED_DATA = "./staged_data/"

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    perror("path already exists")
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

    extracted_id = path_to_input_data.split("/")[-1]

    transcript = read_transcript(path_to_input_data)

    df = to_dataframe(transcript)

    filename = STAGED_DATA+extracted_id+".csv"

    df.to_csv(filename, index=False)
    assert os.path.isfile(filename), "error: could not save preprocess data" 

    return df

def main():
    setup_preprocessing()
    df = preprocess(sys.argv[1])

if __name__ == "__main__":
    main()

