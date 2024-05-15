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
Clippi is a video editing and production tool that aims to capture moments of interest to generate highlight videos from long form content (podcasts, streams etc.)

## Features
### Capture moments of interest
Clippi leverages ML pipelines to perform in-depth analysis on text, audio, and visual data. With the combination of this metadata, Clippi is produces a "weight embedding" that allows it to make a decision as to whether or not the moment in the video is worth saving.

### Analyze metadata to deliver in-depth content analysis
With clips that are of interest, Clippi can leverage the metadata from the preprocessing stage to generate descriptions varying in depth depending on the use case. (descriptions, captions, chapters, summaries etc.)

### Produce Videos
Clippi ships with a video production pipeline that allows it to take the weighted clips and combine them in order to create highlight videos. 

## Architecture
![ClippiRoadmap2 0(2)](https://github.com/cameronslee/clippi/assets/29127398/65af2420-c74d-4221-ab82-b5db808462f1)


## Usage
install from source
```
λ git clone https://github.com/cameronslee/clippi.git
λ cd clippi
```

activate virtual environment
```
λ source ./activate.sh
```

build packages
```
λ ./build.sh
```

run
```
λ python3 clippi.py 
```

# Final Notes
This project is still in development. 
