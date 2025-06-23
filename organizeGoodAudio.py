import os.path
import re

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"
ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
GOOD_FOLDERS_NAMES_TXT_PATH = os.path.join(AUDIOS_PATH, "goodFoldersNames.txt")
TRANSLATED_NAMES_TXT_PATH = os.path.join(AUDIOS_PATH, "translatedNames.txt")

good_names = {}

with open(GOOD_FOLDERS_NAMES_TXT_PATH, "r") as good_folders_file:
    with open(TRANSLATED_NAMES_TXT_PATH, "r") as translated_file:
        while True:
            good_folder = good_folders_file.readline().rstrip()
            if not good_folder:
                break
            translated_name = translated_file.readline().rstrip()
            good_names[good_folder] = translated_name

LIMIT = 1000
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

for item in used_names.items():
    print(item)
