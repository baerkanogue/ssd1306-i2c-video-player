#!/bin/bash

output_file=output/video.oled
mcu_video_file=:video.oled

python converter.py

mpremote rm -r $mcu_video_file
mpremote cp $output_file $mcu_video_file

rm -r $output_file

echo Now playing...
mpremote run mcu.py

