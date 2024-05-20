import sys
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from weight import weight_clips


PREPROCESSING_OUTPUT_DIR = "./"
TEST_INPUT_1 = "./test_in_weight.csv"
TEST_OUTPUT_1 = "./test_out_weight.csv"
WEIGHTED_OUTPUT_FILE = 'out_weighted.csv'

def test_weight_clips():
    test_out = pd.read_csv(TEST_OUTPUT_1)
    out = weight_clips(input_file=TEST_INPUT_1, output_file=WEIGHTED_OUTPUT_FILE, output_dir=PREPROCESSING_OUTPUT_DIR)
    assert test_out.equals(out) == 0

