import pandas as pd
from helpers import perror

# the heart and soul of the clipping algorithm: a vectorized version of maximum subarray sum
def mss(a):
    start = 0
    end = 0
    curr_max = 0
    prev_max = 0
    start_o = 0

    prev_max = a[0]
    
    for i in range(0, len(a)):
        curr_max += a[i]
        if curr_max < 0:
            start = i+1
            curr_max = 0
        elif curr_max > prev_max:
            end = i 
            start_o = start
            prev_max = curr_max

    return start_o, end

def make_clips(input_file, output_file, output_dir):
    try:
        df = pd.read_csv(input_file)
    except:
        perror("could not read " + input_file)
        exit(1)

    try:
        weights = df['weight'].tolist()
        clip = mss(weights)
        print(df['start_time'][clip[0]], df['end_time'][clip[1]])
    except:
        perror("could not generate clip") 
        exit(1)


    return df['start_time'][clip[0]], df['end_time'][clip[1]]

