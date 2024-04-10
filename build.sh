#!/usr/bin/env bash

# distribution
#pyinstaller -F clippy.py

# spacy support, see preprocessing.py
python3 -m spacy download en_core_web_lg

pip3 install -r requirements.txt
pip3 freeze > requirements.txt


