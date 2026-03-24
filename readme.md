# Overview


## Converter
Takes a **video file** from the computer, converts it to **1-bit monochrome with optional dithering**, then turns it into a custom file format compatible with **SSD1306 OLED** displays.


## MCU
Plays the custom video on an **I2C connected SSD1306 OLED** display. The script assumes a wiring configuration of the MCU and the I2C OLED using the default I2C pins. To match your configuration, please edit *[mcu.py](./mcu.py)*. The OLED video will be capped at the original video's framerate (max ~75FPS).


https://github.com/user-attachments/assets/31393b4c-303f-4b38-9923-0db39c0304e6


# Running

## Requirements

|Packages|Infos|
|:---:|:---:|
|av, ImageIO|Extract frames from video|
|pillow|Frames to monochrome and dither|
|mpremote, pyserial|Connect to the MCU|
|ssd1306|SSD1306 library for the MPC|
|colorama|Debug|
|numpy, platformdirs|Internal dependencies|

See *[requirements.txt](./requirements.txt)*.

To install dependencies and prepare Python to execute the scripts:
```sh
# Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```powershell
# Windows
py -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

Now you need to be sure mpremote has a connection to a MCU with MicroPython firmware:
```sh
mpremote connect auto
```

You'll also have to install the [SSD1306 library from MicroPython-lib](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py) on the MCU:
```sh
mpremote mip install ssd1306
```

## Linux
You can directly run *[convert_and_run.sh](./convert_and_run.sh)*. It will automatically call the converter, copy the video to the connected MCU, and run the video.

## Windows
```powershell
py converter.py

mpremote rm :video.oled
mpremote cp .\output\video.oled :video.oled

Remove-Item .\output\video.oled

mpremote run mcu.py
```

