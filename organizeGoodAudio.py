import os.path

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"
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

for item in good_names.items():
    print(item)