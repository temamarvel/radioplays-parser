import os
from pathlib import Path
from colored import Fore, Back, Style
import math

root_path = "audio/"
os.chdir(root_path)

root_folders = list(filter(lambda x: os.path.isdir(x), os.listdir()))
root_folders_count = len(root_folders)

print(f"{Fore.yellow}Root folders count = {root_folders_count}{Style.reset}")

print()

good_count = 0
bad_count = 0

for folder in root_folders:
    if not os.path.isdir(f"{folder}"):
        continue

    subfolders = os.listdir(f"{folder}")
    filtered_folder = list(filter(lambda x: os.path.isdir(os.path.join(folder,x)) , subfolders))
    filtered_mp3 = Path(folder).glob("*.mp3")
    folders_count = len(filtered_folder)
    mp3_count = len(list(filtered_mp3))

    if folders_count == 0 and mp3_count == 1:
        good_count += 1
        print(f"{Fore.green}{folder} [{folders_count}/{mp3_count}]{Style.reset}")
    else:
        bad_count += 1
        print(f"{Fore.red}{folder} [{folders_count}/{mp3_count}]{Style.reset}")

print()

def percent(count):
    return math.ceil(count / (root_folders_count / 100))

print(f"{Fore.green}good_count = {good_count} [{percent(good_count)}%]{Style.reset}")
print(f"{Fore.red}bad_count = {bad_count} [{percent(bad_count)}%]{Style.reset}")