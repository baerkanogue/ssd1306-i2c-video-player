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
    video_path: str = "video.oled"
    FRAME_SIZE: int = 1024

    while True:
        with open(video_path, "rb") as video_file:
            while True:
                frame = video_file.read(FRAME_SIZE)
                if not frame:
                    break

                oled.buffer[:] = frame
                oled.show()
        if not loop:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt...")
