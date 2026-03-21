import os
import shutil
import imageio.v3 as imageiov3
from PIL import Image
from pathlib import Path
from colorama import Fore


def main() -> None:
    TMP_FRAMES_DIR: str = ".tmp"
    OUTPUT_DIR: str = "output"
    OLED_RESOLUTION_WIDTH_HEIGHT: tuple[int, int] = (128, 64)

    make_dirs(TMP_FRAMES_DIR, OUTPUT_DIR)
    extract_frames(TMP_FRAMES_DIR)
    process_frames(TMP_FRAMES_DIR, OUTPUT_DIR, OLED_RESOLUTION_WIDTH_HEIGHT)

    shutil.rmtree(TMP_FRAMES_DIR)

    print(f"Video outputted in {Path(OUTPUT_DIR).resolve()}")


def make_dirs(tmp_frames_dir: str, output_dir: str) -> None:
    try:
        os.makedirs(tmp_frames_dir)
        os.makedirs(output_dir)
    except OSError:
        pass


def get_video_path() -> str:
    return input("Enter video path: ").strip("\"' ")


def extract_frames(output_dir: str) -> None:
    safe_path: Path = Path(output_dir, "frame")
    while True:
        try:
            for index, frame in enumerate(
                imageiov3.imiter(get_video_path(), plugin="pyav")
            ):
                imageiov3.imwrite(f"{safe_path}_{index:04d}.png", frame)
            return
        except Exception as error:
            color_print(error, Fore.RED)


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


def process_frames(
    tmp_dir: str, output_dir: str, oled_resolution_width_height: tuple[int, int]
) -> None:
    while True:
        dither_input: str = input("Use dither ? [Y/n]: ").lower()
        if dither_input in ("", "y"):
            dither: Image.Dither = Image.Dither.FLOYDSTEINBERG
            break
        elif dither_input == "n":
            dither: Image.Dither = Image.Dither.NONE
            break

    tmp_path: Path = Path(tmp_dir)
    output_path: Path = Path(output_dir, "video.oled")

    with open(output_path, "wb") as video_file:
        for image_path in sorted(tmp_path.glob("*.png")):
            image: Image.Image = Image.open(image_path)
            image = image.resize(oled_resolution_width_height).convert(
                mode="1", dither=dither
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
