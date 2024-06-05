```
 .d8888b.  888 d8b                   d8b 
d88P  Y88b 888 Y8P                   Y8P 
888    888 888                           
888        888 888 88888b.  88888b.  888 
888        888 888 888 "88b 888 "88b 888 
888    888 888 888 888  888 888  888 888 
Y88b  d88P 888 888 888 d88P 888 d88P 888 
 "Y8888P"  888 888 88888P"  88888P"  888 
                   888      888          
                   888      888          
                   888      888          

A tool for capturing moments of interest
```

# Overview
Clippi is a video editing and production tool that aims to capture moments of interest in long form content (podcasts, streams etc.)

## Features
### Capture moments of interest
Clippi leverages ML pipelines and media processing algorithms to perform in-depth analysis on text, audio, and visual data. Clippi uses this metadata to produce a "weight embedding" that allows it to make a decision as to whether or not the moment in the video is worth exploring. The clips of interest are delivered as timestamp indices for ease of use.

### Analyze metadata to deliver in-depth content analysis
With clips that are of interest, Clippi can generate natural language varying in depth depending on the use case. (descriptions, captions, chapters, summaries etc.)

## Architecture
![ClippiRoadmap2 0(2)](https://github.com/cameronslee/clippi/assets/29127398/65af2420-c74d-4221-ab82-b5db808462f1)

## Usage
install from source
```
λ git clone https://github.com/cameronslee/clippi.git
λ cd clippi
```

install packages
```
λ pip install -r requirements.txt
```

run
```
λ python3 /clippi/clippi.py 
```

#### Docker
```
λ docker build -t clippi . 
λ docker run -dit clippi 
λ docker ps -a 

# can attach to the session with the following:
λ docker exec -it <container_name> bash
```

# Final Notes
This project is still in development. 
