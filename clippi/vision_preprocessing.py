import numpy as np
import pandas as pd
from tqdm import tqdm
import cv2 as cv 
import threading
import queue
import math

def get_avg_pixel_val(frame: np.ndarray) -> float:
    total_pixel_val = frame.size
    return frame.sum() / total_pixel_val

class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue(maxsize=20)

    def decode(self, video_path, frame_indicies, callback):
        self.queue.put((video_path, frame_indicies, callback))

    def run(self):
        video_path, frame_indicies, on_decode_callback = self.queue.get()
        cap = cv.VideoCapture(video_path)
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_indicies[0])
        success = cap.grab()

        i, count = 0, frame_indicies[0]
        while success:
            if count == frame_indicies[i]:
                success, image = cap.retrieve()
                if success:
                    on_decode_callback(image)
                else:
                    break
                i += 1
                if i >= len(frame_indicies):
                    break
            count += 1
            success = cap.grab()

def preprocess_vision(input_file, output_file, output_dir, num_threads=4, sample_rate=32):
    """
    multithreaded routine to evaluate change in hsv space 

    returns the avg difference between prev frames as vision score

    input_file: src file  
    output_file: dest file 
    output_dir: dest dir 
    num_threads: # of worker threads to read per frame
    sample_rate: # of frames to sample per callback 
    """

    cap = cv.VideoCapture(input_file)
    fps = cap.get(cv.CAP_PROP_FPS)      
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print("Processing: " + input_file + " duration: " + str(duration) + " fps: " + str(fps))

    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    threads = []
    frame_indicies = list(range(0, total_frames, sample_rate))
    tasks = [[] for _ in range(0, num_threads)] 
    frame_per_thread = math.ceil(len(frame_indicies) / num_threads)

    # store frame numbers that threads are responsible for
    for i, frame_num in enumerate(frame_indicies):
        tasks[math.floor(i / frame_per_thread)].append(frame_num)

    for _ in range(0, num_threads):
        w = Worker()
        threads.append(w) 
        w.start()

    results = queue.Queue(maxsize=1000) 
    on_done = lambda x: results.put(x)

    # puts each task into queue with a given callback
    for i, w in enumerate(threads):
        w.decode(input_file, tasks[i], on_done)

    res = []
    backref, completed_threads = 0, 0
    with tqdm(total=num_threads, desc="processing frames") as pbar:
        while completed_threads < num_threads:
            try:
                image = results.get(timeout=2)
                hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
                curr = get_avg_pixel_val(hsv)
                if backref:
                    res.append((curr-backref) / 1000)  # vision score
                    backref = curr
                else:
                    res.append(0)
                    backref = curr 

            except queue.Empty:
                completed_threads += 1
                pbar.update(1)

    df = pd.DataFrame({'start_frame': frame_indicies, 'vision_score': res})
    df['start_time'] = df['start_frame'].apply((lambda x: x / fps))
    df.to_csv(output_dir + output_file, index=False) 
    print("vision preprocessing complete")
