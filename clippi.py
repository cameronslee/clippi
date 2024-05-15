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

from helpers import perror
from text_preprocessing import preprocess_text
from vision_preprocessing import preprocess_vision
from preprocessing import preprocess_all

PREPROCESSING_OUTPUT_DIR = "./cache/"
# preprocessing file handles
VISION_OUTPUT_FILE = 'out_vision_preprocessing.csv'
TEXT_OUTPUT_FILE = 'out_text_preprocessing.csv'

# TODO support batching of multiple videos
usage_string = """
usage: clippi [-h | --help] <command> [<args>] 

args: [<filename>]

commands:
    run [<filename>]                        run clippi from start to finish
    preprocess [<filename>]                 run clippi's entire preprocessing pipeline
    vision_preprocess [<filename>]          run clippi's vision preprocessing pipeline
    text_preprocess [<filename>]            run clippi's text preprocessing pipeline
    audio_preprocess [<filename>]           run clippi's audio preprocessing pipeline
"""

def usage():
    print(usage_string)

# set up dirs needed to perform preprocessing
# handle cache and prefetched files
def setup():
    pass

def main():
    if len(sys.argv) < 3:
        usage()
        exit(1)

    cmd = sys.argv[1]
    arg1 = sys.argv[2]

    # FIXME add checking for filetype 
    if not os.path.isfile(arg1):
        perror("unable to process input file " + str(arg1))
        exit(1)

    match cmd:
        case "run":
            perror("unsupported command")
            exit(1)
        case "preprocess":
            # TODO run entire preprocessing pipeline (includes merging data)
            preprocess_all(input_file=arg1, text_output_file=TEXT_OUTPUT_FILE, vision_output_file=VISION_OUTPUT_FILE, output_dir=PREPROCESSING_OUTPUT_DIR)
        case "vision_preprocess":
            preprocess_vision(input_file=arg1, output_file='out_vision_preprocessing.csv', output_dir=PREPROCESSING_OUTPUT_DIR)
        case "text_preprocess":
            preprocess_text(input_file=arg1, output_file='out_text_preprocessing.csv', output_dir=PREPROCESSING_OUTPUT_DIR)
        case "audio_preprocess":
            perror("unsupported command")
            exit(1)
        case _:
            usage()
            exit(1)

if __name__ == "__main__":
    main()
