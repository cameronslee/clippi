#!/usr/bin/env bash

# distribution
#pyinstaller -F clippy.py

pip3 install -r requirements.txt
pip3 freeze > requirements.txt


