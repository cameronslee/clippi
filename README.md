```
  .d8888b.  888 d8b                            
 d88P  Y88b 888 Y8P                            
 888    888 888                                
 888        888 888 88888b.  88888b.  888  888 
 888        888 888 888 "88b 888 "88b 888  888 
 888    888 888 888 888  888 888  888 888  888 
 Y88b  d88P 888 888 888 d88P 888 d88P Y88b 888 
  "Y8888P"  888 888 88888P"  88888P"   "Y88888 
                    888      888           888 
                    888      888      Y8b d88P 
                    888      888       "Y88P"  

A tool for tokenizing moments of interest in videos
```

## Clippy aims to address the two following use cases:

### Tokenizing moments of interest in videos

### Creating descriptions for timestamps
- This will involve a reduce algorithm that can squash nodes (containing a "topic" embedding)

# Stretch goals:
- video analyzing (for clips where speech is not the deciding factor for a clip being of interest)
- ui 
- highlight video generator
- auto upload

## Usage
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
λ python3 clippy.py 

# for distribution build
λ cd build/dist
λ ./clippy <args>
```


