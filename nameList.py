import os
from colored import Fore, Back, Style

good_folder = 'audio/!GOOD_AUDIO'
os.chdir(good_folder)

folders = os.listdir()

file_names = []

for folder in folders:
    # print(f"{Fore.blue}Folder {folder}{Style.reset}")
    if not os.path.isdir(folder):
        continue

    file_names.append(os.listdir(folder))
    # print(f"\t{os.listdir(folder)}")

for name in sorted(file_names):
    print(name)