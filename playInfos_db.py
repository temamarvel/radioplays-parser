import os

from db_Alchemy import add_item_to_database
from db_models import PlayInfo
from colored import Fore, Back, Style

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
IMAGES = "melodyparser/images"

def remove_brackets(name: str):
    return name.split('[')[0]

audio_folders = sorted(os.listdir(ORGANIZED_PATH))
image_folders = sorted(os.listdir(IMAGES))

for audio_folder in audio_folders:
    if not os.path.isdir(os.path.join(ORGANIZED_PATH, audio_folder)):
        continue

    name = audio_folder
    title = remove_brackets(name)

    # playInfo = PlayInfo(name=name, title=title)
    # add_item_to_database(playInfo)

    has_main_cover = False
    for image_folder in image_folders:
        if title in image_folder:
            has_main_cover = True
            break

    if has_main_cover:
        print(f"{Fore.green}The {audio_folder} has main cover!{Style.reset}")
    else:
        print(f"{Fore.red}The {audio_folder} doesn't have main cover!{Style.reset}")