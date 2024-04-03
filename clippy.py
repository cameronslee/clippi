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

### === GLOBALS === ###


### === PATHS === ###
CWD = os.getcwd()
TRANSCRIPTS_DIR = CWD + "/transcripts/"

### === Prompts === ###
tokenize_prompt = """
    Description TODO

    Args:


    Returns:
    """

get_description_prompt = """
    Description TODO

    Args:

    Returns:
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
# This function needs to follow the following edge cases:
#           generated and manual transcripts (keep track of stream chat/ chat from other platforms
#           no transcript available - perror and return to the user
def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    if transcript_list == None:
        perror("get_transcript() unable to fetch transcript for id: " + video_id)
        exit(1)

    transcript_manual = transcript_list.find_manually_created_transcript(['en']).fetch()
    for i in transcript_manual:
        print(i)
    transcript_generated = transcript_list.find_generated_transcript(['en']).fetch()
    for i in transcript_generated:
        print(i)
    return transcript_generated


# compress each transcript translation by timestamp 
# returns a dictionary of transcripts
# Coalescing done by simple sliding window with a seek ahead node
def transcript_compress():
    # TODO test and refactor prompt engineering 
    compress_prompt = """
    Given a transcript for a video in the form of a list where each entry is a dictionary containing information at a specific
    timestamp in the video, return a list where the entries are combined if they are relatedd and given a description as an 
    additional field in the entry.

    Args:

        transcript (list): A list of dictionaries where each entry contains 'text', 'start', and 'duration'. Each of these entries make up a timestamp in the transcript

        tags (str): A list of tags that help to describe the video. Optional

        restraints (str): A list of restraints to help filter out noise. Optional

        ai_model (str): The AI model to use for natural language processing. Optional, will use default if not provided

    Returns:

        transcript (list): the compressed list of dictionaries where each entry contains text, start, duration and description.

    """
    pass

# Assign weights to each of the nodes in the transcript.
# at this point, the transcript should be "compressed" at this point
def tokenize(transcript):
    pass

### === Driver === ###
# Usage message 
usage_string = """
usage: clippy [-h | --help] <command> [<args>] 

commands:
get transcript 
   transcript <video-url> [-s]        Stage changes to cache. 
      -s : saves the file to the transcripts directory 
"""

def usage(msg=""):
    print(usage_string)

    if msg != "":
        print(msg)

# Sets up clippy
def setup():
    # setup file directory for transcripts
    mkdir(TRANSCRIPTS_DIR)
    print("clippy: setup complete")

def main():
    # setup
    setup()

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
            '''
            if len(sys.argv) == 4:
                arg1 = sys.argv[2]
                if arg1 == '-s':
                    # write t transcript file
                    
                else: 
                    # print the usage for the flags on the transcript command 
                    # refactor for just the usage of the transcript file
                    usage()
            '''

            TEST_URL = "https://www.youtube.com/watch?v=Y-0yZ1AHb0s"
            curr_id = parse_url(TEST_URL)
            transcript = get_transcript(curr_id)

            # TODO consider refactoring into a pandas dataframe

            # Write to file
            new_file = TRANSCRIPTS_DIR + curr_id
            with open(new_file, 'w') as f:
                for t in transcript:
                    f.write(str(t)+'\n')
                f.close()

            assert os.path.isfile(new_file), perror("could not write" + curr_id + "to file")

if __name__ == "__main__":
    main()
