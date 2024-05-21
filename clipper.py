import pandas as pd
from helpers import perror
from moviepy.editor import VideoFileClip

# mac booshit
# https://github.com/Zulko/moviepy/issues/1158
import platform
import os
if platform.system() == 'Darwin':
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

# the heart and soul of the clipping algorithm: a vectorized version of maximum subarray sum
def mss(arr):
    res = []
    for i in range(len(arr)):
        sum = 0
        for j in range (i,len(arr)):
            sum += arr[j]
            res.append((sum, i, j, j-i))

    res.sort(reverse=True)
    return res

def make_clips(video_file, input_file, output_file, output_dir):
    try:
        df = pd.read_csv(input_file)
    except:
        perror("could not read " + input_file)
        exit(1)

    try:
        weights = df['weight'].tolist()
        print("mss length: ", len(mss(weights)))
        clip = mss(weights)[0]
        print(df['start_time'][clip[1]], df['end_time'][clip[2]])
    except:
        perror("could not generate clip") 
        exit(1)

    v = VideoFileClip(video_file)

    best_clip = v.subclip(df['start_time'][clip[1]], df['end_time'][clip[2]])
    best_clip.write_videofile(output_dir+output_file,  codec="libx264", audio_codec="aac")

