#  .d8888b.  888 d8b                            
# d88P  Y88b 888 Y8P                            
# 888    888 888                                
# 888        888 888 88888b.  88888b.  888  888 
# 888        888 888 888 "88b 888 "88b 888  888 
# 888    888 888 888 888  888 888  888 888  888 
# Y88b  d88P 888 888 888 d88P 888 d88P Y88b 888 
#  "Y8888P"  888 888 88888P"  88888P"   "Y88888 
#                    888      888           888 
#                    888      888      Y8b d88P 
#                    888      888       "Y88P"  
#
# Clippy - A utility for tokenizing moments of interest in videos

### === Helpers === ###
# Create file and set timestamp
def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    perror("path already exists")
    return

def init():
    # setup file directory for transcripts
    pass

### === Driver === ###
def main():
    # setup

    # call endpoint for transcript

    # build embedding table for weighting the transcripts
    # each timestamp will represent a node 

    # prompt - call create_descriptions() or create_embeddings() 

    # generate output

    pass

if __name__ == "__main__":
    main()
