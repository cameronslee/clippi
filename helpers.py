import os

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

def clear_cache(cache_dir, paths=[]):
    for p in paths:
        if os.path.isdir(p):
            os.rmdir(p)
        elif os.path.exists(cache_dir + p):
            os.remove(cache_dir + p)
