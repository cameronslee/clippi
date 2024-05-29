import sys
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from weight import weight_clips

from conf import TEST_DIR, WEIGHTED_OUTPUT_FILE
from helpers import mkdir

if len(sys.argv) != 4:
    print("test_weight.py input-file> <test-output>")
    exit(1)

WEIGHT_OUTPUT_DIR = TEST_DIR + "./weight_output"
mkdir(WEIGHT_OUTPUT_DIR)
TEST_INPUT = sys.argv[1]
TEST_OUTPUT = sys.argv[2]

def test_weight_clips():
    test_out = pd.read_csv(TEST_OUTPUT)
    out = weight_clips(input_file=TEST_INPUT, output_file=WEIGHTED_OUTPUT_FILE, output_dir=WEIGHT_OUTPUT_DIR)
    assert test_out.equals(out) == 0

