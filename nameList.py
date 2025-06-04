import os
from colored import Fore, Back, Style

GOOD_FOLDER_PATH = 'audio/!GOOD_AUDIO'
os.chdir(GOOD_FOLDER_PATH)

folders = os.listdir()

file_names = []

for folder in folders:
    if not os.path.isdir(folder):
        continue
    file_names.append(os.listdir(folder))

for name in sorted(file_names):
    print(name)