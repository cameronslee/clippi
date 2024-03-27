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

from youtube_transcript_api import YouTubeTranscriptApi

### === Prompts === ###
tokenize_prompt = """
        foobar
    """

get_description_prompt = """
        barfoo
    """

### === Error Handles === ###
def perror(msg):
    print("error: " + msg)

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

# TODO overload func with list of video_ids as well as lang of transcript
def get_transcript(video_id):
    res = YouTubeTranscriptApi.get_transcript(video_id)

    return res

def init():
    # setup file directory for transcripts
    pass

def tokenize(transcript):
    pass

# Usage message 
usage_string = """
usage: clippy [-h | --help] <command> [<args>] 

commands:
get transcript 
   transcript <video-url>         Stage changes to cache
"""

def usage(msg=""):
    print(usage_string)

    if msg != "":
        print(msg)

# returns the ID of the video 
def parse_url(url):
    i = url.rfind('=')
    # Slice the string up to that index
    res = url[i+1:] if i != -1 else i 

    if i == -1:
        perror("unable to retrieve video ID")
        exit(1)

    return res

### === Driver === ###
def main():
    # setup

    # call endpoint for transcript

    # build embedding table for weighting the transcripts
    # each timestamp will represent a node 

    # prompt - call create_descriptions() or create_embeddings() 

    # generate output

    if len(sys.argv) < 2:
        usage()
        exit(1)

    cmd = sys.argv[1]

    match cmd:
        case "-h":
            usage()
        case "--help":
            usage()
        case "transcript":
            transcript = get_transcript(parse_url(url))

            for i in transcript:
                print(i)

if __name__ == "__main__":
    main()
