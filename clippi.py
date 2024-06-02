"""
 .d8888b.  888 d8b                   d8b 
d88P  Y88b 888 Y8P                   Y8P 
888    888 888                           
888        888 888 88888b.  88888b.  888 
888        888 888 888 "88b 888 "88b 888 
888    888 888 888 888  888 888  888 888 
Y88b  d88P 888 888 888 d88P 888 d88P 888 
 "Y8888P"  888 888 88888P"  88888P"  888 
                   888      888          
                   888      888          
                   888      888          

A tool for capturing moments of interest
"""
import sys
import os

from helpers import clear_cache, perror
from preprocessing import preprocess_all
from weight import weight_clips
from clipper import make_clips
from conf import setup, PREPROCESSING_OUTPUT_DIR, CLIPPED_OUTPUT_DIR, VISION_OUTPUT_FILE, TEXT_OUTPUT_FILE, PREPROCESSING_OUTPUT_FILE, WEIGHTED_OUTPUT_FILE

usage_string = """
usage: clippi [-h | --help] <command> [<args>] 

args: [<filename>]

commands:
    run <filename> [num_clips] [lower_bound] [upper_bound]     run clippi from start to finish 
                                                               options to provide bounds on clip size and 
                                                               number of clips to generate
    preprocess <filename>                                      run clippi's entire preprocessing pipeline
    weight <filename>                                          run clippi's weighting algorithm 
    vision_preprocess <filename>                               run clippi's vision preprocessing pipeline
    text_preprocess <filename>                                 run clippi's text preprocessing pipeline
    audio_preprocess <filename>                                run clippi's audio preprocessing pipeline
    clear_cache                                                clear clippi's cache 
"""

def usage():
    print(usage_string)

def main():
    if len(sys.argv) < 2:
        usage()
        exit(1)

    cmd = sys.argv[1]
    arg1, arg2, arg3, arg4 = "",0,0,0
    if len(sys.argv) >= 3:
        arg1 = sys.argv[2]
        if not os.path.isfile(arg1):
            perror("unable to process input file " + str(arg1))
            exit(1)
    if len(sys.argv) >= 4:
        arg2 = int(sys.argv[3])
    if len(sys.argv) >= 5:
        arg3 = float(sys.argv[4])
    if len(sys.argv) == 6:
        arg4 = float(sys.argv[5])

    match cmd:
        case "run":
            # setup cache dir
            setup(reset=True)
            preprocess_all(input_file=arg1, text_output_file=TEXT_OUTPUT_FILE, vision_output_file=VISION_OUTPUT_FILE, output_dir=PREPROCESSING_OUTPUT_DIR)
            weight_clips(input_file=PREPROCESSING_OUTPUT_DIR+PREPROCESSING_OUTPUT_FILE, output_file=WEIGHTED_OUTPUT_FILE, output_dir=PREPROCESSING_OUTPUT_DIR)
            make_clips(video_file=arg1, input_file=PREPROCESSING_OUTPUT_DIR+WEIGHTED_OUTPUT_FILE, output_dir=CLIPPED_OUTPUT_DIR, num_clips=arg2, lower_bound=arg3, upper_bound=arg4)
        case "clear_cache":
            if clear_cache(PREPROCESSING_OUTPUT_DIR): 
                print("cache cleared")
        case _:
            print(cmd)
            usage()
            exit(1)

if __name__ == "__main__":
    main()
