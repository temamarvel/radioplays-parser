import os
from colored import Fore, Back, Style

good_folder = 'audio/!GOOD_AUDIO'
os.chdir(good_folder)

folders = os.listdir()

with open('goodFoldersNames.txt', 'w') as file:
    print(f"{Fore.blue}The file [goodFoldersNames.txt] is created and open to write.{Style.reset}")
    for folder in sorted(folders):
        file.write(f"{folder}\n")
    print(f"{Fore.blue}All names are writen to file.{Style.reset}")
        