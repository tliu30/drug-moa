#!/bin/bash

STARTDIR='./output'
cd $STARTDIR
python -m SimpleHTTPServer &
chromium-browser http://0.0.0.0:8000/$1/view.html

# python code.py
# chromium-browser http://0.0.0.0:8080
