import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from conf import setup, CACHE_DIR, PREPROCESSING_OUTPUT_DIR, CLIPPED_OUTPUT_DIR, TEST_DIR

def test_setup():
    setup()
    assert os.path.isdir(CACHE_DIR)
    assert os.path.isdir(PREPROCESSING_OUTPUT_DIR)
    assert os.path.isdir(CLIPPED_OUTPUT_DIR)
    assert os.path.isdir(TEST_DIR)

