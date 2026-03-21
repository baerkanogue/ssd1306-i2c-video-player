import os
import shutil
import imageio.v3 as imageiov3
from PIL import Image
from pathlib import Path
from colorama import Fore


def main() -> None:
    OUTPUT_DIR: str = "output"
    OLED_RESOLUTION_WIDTH_HEIGHT: tuple[int, int] = (128, 64)

    make_dirs(OUTPUT_DIR)
    process_frames(OUTPUT_DIR, OLED_RESOLUTION_WIDTH_HEIGHT)

    print(f"Video outputted in {Path(OUTPUT_DIR).resolve()}")


def make_dirs(output_dir: str) -> None:
    try:
        os.makedirs(output_dir)
    except OSError:
        pass


def get_video_path() -> str:
    return input("Enter video path: ").strip("\"' ")


def image_to_oled_bytes(
    image: Image.Image, oled_resolution_width_height: tuple[int, int]
) -> bytearray:
    width: int = oled_resolution_width_height[0]
    height: int = oled_resolution_width_height[1]
    buffer: bytearray = bytearray(width * height // 8)

    pixels = image.load()
    if not pixels:
        raise Exception("image.load() failure")

    for x in range(width):
        for page in range(height // 8):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit

                if pixels[x, y]:
                    byte |= 1 << bit

            buffer[x + page * width] = byte

    return buffer


def choose_dither() -> Image.Dither:
    while True:
        dither_input: str = input("Use dither ? [Y/n]: ").lower()
        if dither_input in ("", "y"):
            return Image.Dither.FLOYDSTEINBERG
        elif dither_input == "n":
            return Image.Dither.NONE


def process_frames(
    output_dir: str, oled_resolution_width_height: tuple[int, int]
) -> None:
    video_path: str = get_video_path()
    OUTPUT_FILE_NAME: str = "video.oled"

    output_path: Path = Path(output_dir, OUTPUT_FILE_NAME)

    with open(output_path, "wb") as video_file:
        for frame in imageiov3.imiter(video_path, plugin="pyav"):
            image: Image.Image = Image.fromarray(frame)
            image = image.resize(oled_resolution_width_height).convert(
                mode="1", dither=choose_dither()
            )

            output_image: bytearray = image_to_oled_bytes(
                image, oled_resolution_width_height
            )
            video_file.write(output_image)


def color_print(message: str | Exception, color: str) -> None:
    print(f"{color}{message}{Fore.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        color_print("\nKeyboard interrupt...", Fore.YELLOW)
