from machine import I2C
from ssd1306 import *
from time import time_ns, sleep


def main() -> None:
    OLED_WIDTH: int = 128
    OLED_HEIGHT: int = 64

    i2c = I2C(freq=int(1e6))
    oled_address: int = i2c.scan()[0]
    print(f"Device found at address {oled_address} ({hex(oled_address)})")

    oled: SSD1306_I2C = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, oled_address)

    try:
        play_video(oled, cap_fps=False)
    except KeyboardInterrupt:
        say_goodbye(oled, OLED_HEIGHT)


def say_goodbye(oled: SSD1306, oled_height: int) -> None:
    print("Exiting...")
    oled.fill(0)
    oled.text("GOODBYE...", 24, oled_height // 2)
    oled.show()
    sleep(3)
    oled.fill(0)
    oled.show()


def play_video(oled: SSD1306, loop: bool = True, cap_fps: bool = True) -> None:
    video_path: str = "video.oled"
    FRAME_SIZE: int = 1024
    METADATA_SIZE: int = 1

    frames_index: int = 0

    with open(video_path, "rb") as video_file:
        start_time_ns: int = time_ns()
        video_fps: int = int.from_bytes(video_file.read(METADATA_SIZE), "big")
        frame_period_ns: int = int(1e9 // video_fps)

        while True:
            frame = video_file.read(FRAME_SIZE)
            if not frame:
                if not loop:
                    break
                video_file.seek(METADATA_SIZE)
                frames_index = 0
                start_time_ns = time_ns()

            oled.buffer[:] = frame
            oled.show()

            frames_index += 1

            after_frame_time_ns: int = time_ns()
            target_time: int = start_time_ns + frames_index * frame_period_ns
            delay_ns: int = target_time - after_frame_time_ns

            if delay_ns > 0 and cap_fps:
                sleep(delay_ns / 1e9)


if __name__ == "__main__":
    main()
