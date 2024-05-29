import os

from helpers import perror, mkdir, clear_cache

HOME_DIR = os.path.expanduser(path='~')
CACHE_DIR = HOME_DIR + "/.clippicache/"

TEST_DIR = CACHE_DIR + "./test/"
PREPROCESSING_OUTPUT_DIR = CACHE_DIR + "./preprocessing/"
CLIPPED_OUTPUT_DIR = CACHE_DIR + "./clips/"

# preprocessing file handles
VISION_OUTPUT_FILE = 'out_vision_preprocessing.csv'
TEXT_OUTPUT_FILE = 'out_text_preprocessing.csv'
# working dataset
PREPROCESSING_OUTPUT_FILE = 'out_preprocessing.csv'
# weighted dataset
WEIGHTED_OUTPUT_FILE = 'out_weighted.csv'

def setup(reset=True):
    if reset:
        try:
            pass
            print(CACHE_DIR)
            clear_cache(cache_dir=CACHE_DIR)
            mkdir(CACHE_DIR)
            mkdir(PREPROCESSING_OUTPUT_DIR)
            mkdir(CLIPPED_OUTPUT_DIR)
            mkdir(TEST_DIR)
        except:
            perror("unable to setup output dirs")
            exit(1)
