import sys

sys.path.append('../clippi/')

from clippi.helpers import mkdir
from clippi.clipper import make_clips 
from clippi.conf import TEST_DIR

if len(sys.argv) != 3:
    print("test_clipper.py <video> <input-file>")
    exit(1)

CLIPPER_OUTPUT_DIR = TEST_DIR + "./clipper_output"
mkdir(CLIPPER_OUTPUT_DIR)
TEST_VIDEO = sys.argv[1]
TEST_INPUT = sys.argv[2]


def test_make_clips():
    res = make_clips(video_file=TEST_VIDEO, input_file=TEST_INPUT, output_dir=CLIPPER_OUTPUT_DIR, lower_bound=5.0, upper_bound=15.0, video_generation=True)
    assert len(res) != 0
    
