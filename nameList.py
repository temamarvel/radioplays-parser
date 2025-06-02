import os
from colored import Fore, Back, Style

good_folder = 'audio/GOOD_AUDIO'
os.chdir(good_folder)

folders = os.listdir()

fileNames = []

for folder in folders:
    # print(f"{Fore.blue}Folder {folder}{Style.reset}")
    if not os.path.isdir(folder):
        continue

    fileNames.append(os.listdir(folder))
    # print(f"\t{os.listdir(folder)}")

for name in sorted(fileNames):
    print(name)