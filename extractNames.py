import os
from colored import Fore, Back, Style

GOOD_FOLDER_PATH = "audio/!GOOD_AUDIO"
OUTPUT_FILE_NAME = "goodFoldersNames.txt"
os.chdir(GOOD_FOLDER_PATH)

folders = os.listdir()

with open(OUTPUT_FILE_NAME, 'w') as file:
    print(f"{Fore.blue}The file [{OUTPUT_FILE_NAME}] is created and open to write.{Style.reset}")
    for folder in sorted(folders):
        file.write(f"{folder}\n")
    print(f"{Fore.blue}All names are writen to file.{Style.reset}")
        