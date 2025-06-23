import os.path
import re
import shutil

from colored import Fore, Back, Style

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"
ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
GOOD_FOLDERS_NAMES_TXT_PATH = os.path.join(AUDIOS_PATH, "goodFoldersNames.txt")
TRANSLATED_NAMES_TXT_PATH = os.path.join(AUDIOS_PATH, "translatedNames.txt")

good_names = {}

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"{Fore.green}The folder {Style.bold}[{folder_path}]{Style.reset} {Fore.green} has created!{Style.reset}")
    else:
        print(f"{Fore.yellow}The folder {Style.bold}[{folder_path}]{Style.reset} {Fore.yellow}has already created!{Style.reset}")

def copy_file(s_path, d_path):
    if os.path.exists(d_path):
        print(
            f"{Fore.yellow}The file {Style.bold}[{d_path}]{Style.reset} {Fore.yellow}has already existed!{Style.reset}")
        return False

    try:
        shutil.copyfile(s_path, d_path)
        print(f"{Fore.green}The file {Style.bold}[{s_path}]{Style.reset} {Fore.green} has successfully copied to {Style.bold}[{d_path}]{Style.reset}{Fore.green}!{Style.reset}")
        return True
    except:
        print(f"{Fore.red}Error! Something went wrong during copying. The file {Style.bold}[{s_path}]{Style.reset}{Fore.red} hasn't copied.{Style.reset}")
        return False


with open(GOOD_FOLDERS_NAMES_TXT_PATH, "r") as good_folders_file:
    with open(TRANSLATED_NAMES_TXT_PATH, "r") as translated_file:
        while True:
            good_folder = good_folders_file.readline().rstrip()
            if not good_folder:
                break
            translated_name = translated_file.readline().rstrip()
            good_names[good_folder] = translated_name

LIMIT = 5
count = 0

used_names = {}

for key, value in good_names.items():
    if count == LIMIT:
        break
    count += 1
    # print(f"key={key}: value={value}")
    key_folder_path = os.path.join(AUDIOS_PATH, key)
    files = os.listdir(key_folder_path)
    for file in files:
        file_name_parts = os.path.splitext(file)
        ext = file_name_parts[1]

        if ext == ".mp3":
            # todo refactor it!!!
            print("----------------------------------------------------------------------------------------------")
            match = re.match(r'^(.*?)\s*\[(.*?)\]', value)
            name = ""
            meta_data = ""
            if match:
                name = match.group(1)
                meta_data = match.group(2)
            else:
                name = value

            if not used_names.get(name):
                used_names[name] = 1
            else:
                used_names[name] += 1

            new_name = f"{name}[v.{used_names[name]}]"

            path_to = os.path.join(ORGANIZED_PATH, new_name)
            create_folder(path_to)

            src_path = os.path.join(key_folder_path, file)
            dst_path = os.path.join(path_to, f"{new_name}{ext}")
            copy_file(src_path, dst_path)

            for f in files:
                f_name_parts = os.path.splitext(f)
                cover_ext = f_name_parts[1]

                if cover_ext == ".mp3":
                    continue

                covers_folder_path = os.path.join(path_to, "Covers")
                create_folder(covers_folder_path)

                src_cover_path = os.path.join(key_folder_path, f)
                dst_cover_path = os.path.join(covers_folder_path, f)
                copy_file(src_cover_path, dst_cover_path)

# for item in used_names.items():
#     print(item)
