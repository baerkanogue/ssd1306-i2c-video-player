#!/bin/bash

python converter.py

mpremote rm -r :video
mpremote mkdir :video
mpremote cp -r video/* :video

# rm -r video

echone Now playing...
mpremote run mcu.py

