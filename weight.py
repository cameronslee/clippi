# Max subarray problem LOL
import pandas as pd
from helpers import perror

"""
clip_weight = sentiment_score + vision_score + num_neighbors
    sentiment_score = max(positive_sentiment, negative_sentiment, neutral_sentiment)
    vision_score = vision_label_scores[vision_classification] 
    num_neighbors = contiguous surrounding neighbors with similar col values - in this case: vision classification
"""
def weight_clips(input_file, output_file, output_dir):
    try:
        df = pd.read_csv(input_file)
    except:
        perror("could not read " + input_file)
        exit(1)
    print(df.info())

    # sentiment score
    def get_sentiment_score(row):
        return max(row['positive_sentiment'], max(row['negative_sentiment'], row['neutral_sentiment']))

    df['sentiment_score'] = df.apply(get_sentiment_score, axis=1)
    
    # replace NANs with neutral score
    # TODO need to fill in start and end frame for data that came from text preprocessing
    df['vision_classification'] = df['vision_classification'].fillna(df['vision_classification'].shift(-1))
    # vision score
    vision_label_scores = { "Highlight Worthy": 1, "Neutral": 0, "Not Highlight Worthy": -1 }
    def get_vision_scores(row):
        return vision_label_scores[str(row['vision_classification'])]

    df['vision_score'] = df.apply(get_vision_scores, axis=1)

    print(df.info())

    # export with scores
    df.to_csv(output_dir + output_file, index=False) 

