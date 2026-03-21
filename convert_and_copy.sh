#!/bin/bash

python converter.py

mpremote cp -r video :video

rm -r video

echo Done