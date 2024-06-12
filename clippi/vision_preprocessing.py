import os
import pandas as pd
from tqdm import tqdm
import cv2 as cv 
import threading
import queue
import math

from helpers import perror

from conf import PREPROCESSING_OUTPUT_DIR, VISION_OUTPUT_FILE

class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue(maxsize=20)

    def decode(self, video_path, frame_indicies, callback):
        self.queue.put((video_path, frame_indicies, callback))

    def run(self):
        """execute frame reading"""
        video_path, frame_indicies, on_decode_callback = self.queue.get()
        cap = cv.VideoCapture(video_path)

        cap.set(cv.CAP_PROP_POS_FRAMES, frame_indicies[0])
        success = cap.grab()

        results = []
        idx, count = 0, frame_indicies[0]
        while success:
            if count == frame_indicies[idx]:
                success, image = cap.retrieve()
                if success:
                    on_decode_callback(image)
                else:
                    break
                idx += 1
                if idx >= len(frame_indicies):
                    break
            count += 1
            success = cap.grab()
# ideas
# detect changes in frame intensity and brightness
# detect changes in HSV color space
def detect():
    pass

### === Dataframe === ###
#df = pd.DataFrame(columns=['start_time', 'end_time', 'start_frame', 'end_frame'])

### === Driver === ###
def preprocess_vision(input_file, output_file, output_dir):
    if not os.path.isfile(input_file):
        perror("unable to process input file " + str(input_file))
        exit(1)

    print("Processing: " + input_file)
    global df
    cap = cv.VideoCapture(input_file)

    tqdm.pandas(desc="Processing Visual Data")
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    sample_rate = 32
    threads = []
    frame_indicies = list(range(0, total_frames, sample_rate))
    num_threads = 4 # num_threads is the number of worker threads to read video frame
    tasks = [[] for _ in range(0, num_threads)] # store frame number for each threads
    frame_per_thread = math.ceil(len(frame_indicies) / num_threads)

    for i, frame_num in enumerate(frame_indicies):
        tasks[math.floor(i / frame_per_thread)].append(frame_num)
    for _ in range(0, num_threads):
        w = Worker()
        threads.append(w) 
        w.start()

    results = queue.Queue(maxsize=1000) 
    on_done = lambda x: results.put(x)

    for i, w in enumerate(threads):
        w.decode(input_file, tasks[i], on_done)

    completed_threads = 0
    while completed_threads < num_threads:
        try:
            image = results.get(timeout=2)
        except queue.Empty:
            completed_threads += 1
        else:
            print(image)

    print("vision preprocessing complete")

    # export
    #df.to_csv(output_dir + output_file, columns=["start_time", "end_time", "start_frame", "end_frame", "vision_classification", "avg_fps"], index=False) 

def main():
    preprocess_vision(input_file="../cache/test1.mp4", output_file=VISION_OUTPUT_FILE, output_dir=PREPROCESSING_OUTPUT_DIR)

if __name__ == "__main__":
    main()
