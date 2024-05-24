import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from clipper import make_clips 

PREPROCESSING_OUTPUT_DIR = "./"
TEST_INPUT_1 = "out_weighted.csv"
OUTPUT_DIR = './clips/'

VIDEO = 'What Mark Zuckerberg learned from Caesar Augustus.mp4'

def test_make_clips():
    res = make_clips(video_file=VIDEO, input_file=TEST_INPUT_1, output_dir=OUTPUT_DIR, lower_bound=5.0, upper_bound=15.0, debug_flag1=True)
    assert len(res) != 0
    
