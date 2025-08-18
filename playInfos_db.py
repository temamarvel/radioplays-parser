import os

from db_Alchemy import add_item_to_database, update_column_in_database
from db_models import PlayInfo
from colored import Fore, Back, Style

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
IMAGES = "melodyparser/images"

def remove_brackets(n: str):
    return n.split('[')[0]

audio_folders = sorted(os.listdir(ORGANIZED_PATH))
image_folders = sorted(os.listdir(IMAGES))

for audio_folder in audio_folders:
    audio_folder_path = os.path.join(ORGANIZED_PATH, audio_folder)
    if not os.path.isdir(audio_folder_path):
        continue

    name = audio_folder
    title = remove_brackets(name)

    # playInfo = PlayInfo(name=name, title=title)
    # add_item_to_database(playInfo)

    # has_main_cover = False
    # for image_folder in image_folders:
    #     if title in image_folder:
    #         has_main_cover = True
    #         break
    covers_path = os.path.join(audio_folder_path, "Covers/Originals/main_cover.webp")

    has_main_cover = os.path.exists(covers_path)

    if has_main_cover:
        print(f"{Fore.green}The {audio_folder} has main cover!{Style.reset}")
        update_column_in_database(name, covers_path)
    else:
        print(f"{Fore.red}The {audio_folder} doesn't have main cover!{Style.reset}")