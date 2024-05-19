# Custom helper functions 

import os

def perror(msg):
    print("error: " + msg)

def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    print("path already exists")
    return

def clear_cache(cache_dir, files = []):
    for f in files:
        if os.path.exists(cache_dir + f):
            os.remove(cache_dir + f)
