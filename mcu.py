import os
from machine import I2C
from ssd1306 import *


def main() -> None:
    OLED_WIDTH: int = 128
    OLED_HEIGHT: int = 64

    i2c = I2C(freq=int(1e6))
    oled_address: int = i2c.scan()[0]

    oled: SSD1306_I2C = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, oled_address)

    play_video(oled)


def play_video(oled: SSD1306, loop: bool = True) -> None:
    video_dir: str = "video"

    while loop:

        for file_name in sorted(os.listdir(video_dir)):
            frame: str = video_dir + "/" + file_name
            oled.buffer[:] = open(frame, "rb").read()
            oled.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt...")
