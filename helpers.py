import os
import shutil

def perror(msg):
    print("error: " + msg)

def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

def mkdir(path, echo=False):
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    if echo:
        print("path already exists")

def clear_cache(cache_dir):
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)
