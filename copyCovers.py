import os
import shutil
from colored import Fore, Back, Style

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"

coverFolders = sorted(os.listdir(COVERS_PATH))
audioFolders = sorted(os.listdir(AUDIOS_PATH))

LIMIT = 4
count = 0

for audioFolder in audioFolders:
    if count == LIMIT:
        break
    count += 1
    audio_full_path = os.path.join(AUDIOS_PATH, audioFolder)

    if not os.path.isdir(audio_full_path):
        continue

    print()
    print(f"{Style.bold}{Fore.blue}{audio_full_path}{Style.reset}")

    mp3_file_name = os.listdir(audio_full_path)[0]
    print(mp3_file_name)

    try:
        coverFolderIndex = coverFolders.index(mp3_file_name)
        coverFolder = coverFolders[coverFolderIndex]
        print(f"{Fore.green}Has cover{Style.reset}")
        cover_full_Path = os.path.join(COVERS_PATH, coverFolder)
        covers = os.listdir(cover_full_Path)
        print(f"{Fore.yellow}{covers}{Style.reset}")
        for cover in covers:
            src = os.path.join(cover_full_Path, cover)
            dst = os.path.join(audio_full_path, cover)
            print(f"{Fore.yellow}Copy from [{src}]{Style.reset}")
            print(f"{Fore.yellow}Copy to [{dst}]{Style.reset}")
            try:
                shutil.copyfile(src, dst)
                print(f"{Fore.green}Done! File copied!{Style.reset}")
            except:
                print(f"{Fore.red}Error! Something went wrong during copying.{Style.reset}")
    except:
        continue


