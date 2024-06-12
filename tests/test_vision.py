import sys

sys.path.append('../clippi/')

from conf import VISION_OUTPUT_FILE, TEST_DIR
from vision_preprocessing import preprocess_vision  

def test_vision():
    preprocess_vision(input_file="../cache/test1.mp4", output_file=VISION_OUTPUT_FILE, output_dir=TEST_DIR)
