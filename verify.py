import os
from pathlib import Path
from colored import Fore, Back, Style

root_path = "audio/"
os.chdir(root_path)

folders = os.listdir()

print(f"{Fore.yellow}Root folders count = {len(folders)}{Style.reset}")

print()

good_count = 0
bad_count = 0

for folder in folders:
    if not os.path.isdir(f"{folder}"):
        continue
    subfolders = os.listdir(f"{folder}")
    filtered_folder = filter(lambda x: os.path.isdir(os.path.join(folder,x)) , subfolders)
    filtered_mp3 = Path(folder).glob("*.mp3")
    folders_count = len(list(filtered_folder))
    mp3_count = len(list(filtered_mp3))

    if folders_count == 0 and mp3_count == 1:
        good_count += 1
        print(f"{Fore.green}{folder} [{folders_count}/{mp3_count}]{Style.reset}")
    else:
        bad_count += 1
        print(f"{Fore.red}{folder} [{folders_count}/{mp3_count}]{Style.reset}")

print()

print(f"{Fore.green}good_count = {good_count}{Style.reset}")
print(f"{Fore.red}bad_count = {bad_count}{Style.reset}")