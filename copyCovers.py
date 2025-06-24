import os
import shutil
from colored import Fore, Back, Style

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"

cover_folders = sorted(os.listdir(COVERS_PATH))
audio_folders = sorted(os.listdir(AUDIOS_PATH))

LIMIT = 500
count = 0

for audioFolder in audio_folders:
    if count == LIMIT:
        break
    count += 1
    audio_full_path = os.path.join(AUDIOS_PATH, audioFolder)

    if not os.path.isdir(audio_full_path):
        continue

    print()
    print(f"{Style.bold}{Fore.blue}{audio_full_path}{Style.reset}")

    files_in_folder = os.listdir(audio_full_path)
    mp3_file_name = files_in_folder[0]
    for file in files_in_folder:
        splitFileName = os.path.splitext(file)
        ext = splitFileName[1]
        if ext == '.mp3':
            mp3_file_name = file
            break

    print(mp3_file_name)

    try:
        cover_folder_index = cover_folders.index(mp3_file_name)
        cover_folder = cover_folders[cover_folder_index]
        print(f"{Fore.green}Has cover{Style.reset}")
        cover_full_Path = os.path.join(COVERS_PATH, cover_folder)
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


