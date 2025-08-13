import os

from db_Alchemy import add_item_to_database
from db_models import PlayInfo

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

def remove_brackets(name: str):
    return name.split('[')[0]

folders = sorted(os.listdir(ORGANIZED_PATH))

for folder in folders:
    if not os.path.isdir(os.path.join(ORGANIZED_PATH, folder)):
        continue

    name = folder
    title = remove_brackets(name)

    playInfo = PlayInfo(name=name, title=title)

    add_item_to_database(playInfo)