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

def make_clips(video_file, input_file, output_file, output_dir):
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

    v = VideoFileClip(video_file)
    # lil post processing 
    fade_duration = 3  # Duration of the fade-out effect in seconds
    v = v.fadein(fade_duration) 
    v = v.audio_fadein(fade_duration)
    v = v.audio_fadeout(fade_duration)
    v = v.fadeout(fade_duration)

    best_clip = v.subclip(df['start_time'][clip[0]], df['end_time'][clip[1]])
    best_clip.write_videofile(output_dir+output_file,  codec="libx264", audio_codec="aac")

