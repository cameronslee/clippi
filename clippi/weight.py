# weight.py
import pandas as pd
from helpers import perror

"""
clip_weight = sentiment_score + vision_score + vision_desire + sentiment_desire
    sentiment_score = max(positive_sentiment, negative_sentiment, neutral_sentiment)
    vision_score = vision_label_scores[vision_classification] 
    vision_desire = CONTIGUOUS surrounding neighbors with same ROW values - in this case: vision_score 
    sentiment_desire = CONTIGUOUS surrounding neighbors with same ROW values - in this case: sentiment_score 
"""
def weight_clips(input_file, output_file, output_dir):
    try:
        df = pd.read_csv(input_file)
    except:
        perror("could not read " + input_file)
        exit(1)

    # sentiment score
    def get_sentiment_score(row):
        return max(row['positive_sentiment'], max(row['negative_sentiment'], row['neutral_sentiment']))

    df['sentiment_score'] = df.apply(get_sentiment_score, axis=1)
     
    # vision score
    THRESHOLD_APPEARANCE = 3
    """
    vision score
        highlight worthy: 1
        neutral: 0
        not highlight worthy: -3              the reason for this being -THRESHOLD_APPEARANCE is to account for noise.
                                              it acts as a threshold variable
                                              this can be thought of as: "lets not consider this section until it 
                                              appears more than THRESHOLD_APPEARANCE times in a row"
    """
    vision_label_scores = { "Highlight Worthy": 1, "Neutral": 0, "Not Highlight Worthy": -THRESHOLD_APPEARANCE }
    def get_vision_scores(row):
        return vision_label_scores[str(row['vision_classification'])]

    df['vision_score'] = df.apply(get_vision_scores, axis=1)

    # vision desire: LSTM-like metric for "given similarity in surrounding frames, how likely are we to take this section?"
    # https://stackoverflow.com/questions/46504138/cumulative-count-reset-on-condition/46504302#46504302
    diff = df['vision_score'].diff().fillna(0).ne(0).cumsum()
    counts = df.groupby(diff)['vision_score'].transform('count')
    df['vision_desire'] = counts / 1000

    # sentiment_desire 
    diff = df['sentiment_score'].diff().fillna(0).ne(0).cumsum()
    counts = df.groupby(diff)['sentiment_score'].transform('count')
    df['sentiment_desire'] = counts / 1000

    # clip weight
    def get_weight(row):
        return row['vision_score'] + row['sentiment_score'] + row['vision_desire'] + row['sentiment_desire'] 
    df['weight'] = df.apply(get_weight, axis=1) 

    # export with scores
    df.to_csv(output_dir + output_file, index=True) 
    
    return df
