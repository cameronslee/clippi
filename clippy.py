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
import os
import sys

### === PATHS === ###
CWD = os.getcwd()
TRANSCRIPTS_DIR = CWD + "/transcripts/"

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

# returns the ID of the video 
def parse_url(url):
    i = url.rfind('=')
    # Slice the string up to that index
    res = url[i+1:] if i != -1 else i 

    if i == -1:
        perror("unable to retrieve video ID")
        exit(1)

    return res

### === Transcript Handles === ###
# TODO overload func with list of video_ids as well as lang of transcript
def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    if transcript_list == None:
        perror("get_transcript() unable to fetch transcript for id: " + video_id)
        exit(1)

    #transcript_manual = transcript_list.find_manually_created_transcript(['en']).fetch()
    #for i in transcript_manual:
         #print(i)

    transcript_generated = transcript_list.find_generated_transcript(['en']).fetch()
    for i in transcript_generated:
        print(i)

    return transcript_generated

### === Driver === ###
# Usage message 
usage_string = """
usage: clippy [-h | --help] <command> [<args>] 

commands:
get transcript 
   transcript <video-url>         fetch transcript via a URL to a Youtube Video
"""

def usage(msg=""):
    print(usage_string)

    if msg != "":
        print(msg)

# setup file directory for transcripts
def setup():
    mkdir(TRANSCRIPTS_DIR)
    print("clippy: setup complete")

def main():
    setup()

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
            if len(sys.argv) != 3:
                usage()
                exit(1)

            curr_id = parse_url(sys.argv[2])
            transcript = get_transcript(curr_id)

            # Write to file
            new_file = TRANSCRIPTS_DIR + curr_id
            with open(new_file, 'w') as f:
                for t in transcript:
                    f.write(str(t)+'\n')
                f.close()

            assert os.path.isfile(new_file), perror("could not write" + curr_id + "to file")
        case _:
            perror(f"'{cmd}' is not a recognized command")

if __name__ == "__main__":
    main()
