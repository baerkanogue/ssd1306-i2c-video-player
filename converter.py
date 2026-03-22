import os
import imageio.v3 as imageiov3
from PIL import Image
from pathlib import Path
from colorama import Fore
from dataclasses import dataclass
from function_timer import print_execution_time
from typing import Any


@dataclass
class ProcessData:
    input_video_path: str | Path
    output_path: str | Path
    oled_resolution_width_height: tuple[int, int]
    dither_mode: Image.Dither


def main() -> None:
    OUTPUT_DIR: str = "output"
    OUTPUT_FILE_NAME: str = "video.oled"
    OLED_RESOLUTION_WIDTH_HEIGHT: tuple[int, int] = (128, 64)

    make_dirs(OUTPUT_DIR)
    output_file_path: Path = Path(OUTPUT_DIR, OUTPUT_FILE_NAME)

    process_data: ProcessData = ProcessData(
        input_video_path=get_video_path(),
        output_path=output_file_path,
        oled_resolution_width_height=OLED_RESOLUTION_WIDTH_HEIGHT,
        dither_mode=choose_dither(),
    )

    process_frames(process_data)

    print(f"Video outputted in {output_file_path.resolve()}")


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

    pixels: Image.core.PixelAccess | None = image.load()
    if pixels is None:
        raise RuntimeError("image.load() failure")

    pages: int = height // 8
    for x in range(width):
        for page in range(pages):
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


@print_execution_time
def process_frames(process_data: ProcessData) -> None:
    video_path: str | Path = process_data.input_video_path
    output_path: str | Path = process_data.output_path
    oled_resolution: tuple[int, int] = process_data.oled_resolution_width_height
    dither_mode: Image.Dither = process_data.dither_mode

    imageiov3_plugin: str = "pyav"

    metadata: dict[str, Any] = imageiov3.immeta(video_path, plugin=imageiov3_plugin)
    print(metadata.get("fps"))

    with open(output_path, "wb") as video_file:
        for frame in imageiov3.imiter(video_path, plugin=imageiov3_plugin):
            image: Image.Image = Image.fromarray(frame)
            image = image.resize(oled_resolution).convert(mode="1", dither=dither_mode)

            output_image: bytearray = image_to_oled_bytes(image, oled_resolution)
            video_file.write(output_image)


def color_print(message: str | Exception, color: str) -> None:
    print(f"{color}{message}{Fore.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        color_print("\nKeyboard interrupt...", Fore.YELLOW)
