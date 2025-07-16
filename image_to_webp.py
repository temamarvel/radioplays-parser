import os

from PIL import Image
from PIL.Image import Resampling
from colored import Fore, Back, Style

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
ORIGINALS = "Originals"
THUMBNAILS = "Thumbnails"

os.chdir(ORGANIZED_PATH)

root_folders = sorted(os.listdir())

def convert_original(image, path, webp_path):
    if os.path.exists(webp_path):
        print(f"{Fore.yellow}The image {original_webp_path} is already exists. The processing skipped.{Style.reset}")
        return

    try:
        image.save(webp_path, format="WEBP", quality=85)
        print(f"{Fore.green}The image {path} is converted and saved to {webp_path}{Style.reset}")
    except:
        print(f"{Fore.red}ERROR! Something wrong during convertion file {path}{Style.reset}")

def convert_thumbnail(image, path, webp_path):
    if os.path.exists(webp_path):
        print(f"{Fore.yellow}The image {webp_path} is already exists. The processing skipped.{Style.reset}")
        return

    try:
        thumbnail_img = image.copy()
        thumbnail_img.thumbnail((200, 200), Resampling.LANCZOS)
        thumbnail_img.save(webp_path, format="WEBP", quality=85)
        print(
            f"{Fore.green}The image (thumbnail) {path} is converted and saved to {webp_path}{Style.reset}")
    except:
        print(f"{Fore.red}ERROR! Something wrong during convertion file {path}{Style.reset}")

for folder in root_folders:
    if not os.path.isdir(folder):
        continue

    covers_folder_path = os.path.join(folder, "Covers")

    if not os.path.exists(covers_folder_path):
        continue

    covers = os.listdir(covers_folder_path)

    originals_path = os.path.join(covers_folder_path, ORIGINALS)
    thumbnails_path = os.path.join(covers_folder_path, THUMBNAILS)

    if not os.path.exists(originals_path):
        os.makedirs(originals_path)
    if not os.path.exists(thumbnails_path):
        os.makedirs(thumbnails_path)

    # print(covers)

    for cover in covers:
        if cover == ".DS_Store":
            continue

        cover_path = os.path.join(covers_folder_path, cover)

        if os.path.isdir(cover_path):
            continue

        with Image.open(cover_path) as img:
            name, ext = os.path.splitext(cover)

            original_webp_path = os.path.join(originals_path, f"{name}.webp")
            convert_original(img, cover_path, original_webp_path)

            thumbnail_webp_path = os.path.join(thumbnails_path, f"{name}_thumb.webp")
            convert_thumbnail(img, cover_path, thumbnail_webp_path)