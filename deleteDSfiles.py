import os

COVERS_PATH = "audio/!COVERS"
AUDIOS_PATH = "audio/!GOOD_AUDIO"
ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

folders = sorted(os.listdir(ORGANIZED_PATH))

for folder in folders:
    if folder == '.DS_Store':
        folder_full_path = os.path.join(ORGANIZED_PATH, folder)
        print(folder_full_path)
        os.remove(folder_full_path)
        print(f"File [{folder_full_path}] is deleted!")
        print()


    folder_full_path = os.path.join(ORGANIZED_PATH, folder)
    print(folder_full_path)

    if not os.path.isdir(folder_full_path):
        continue

    files = os.listdir(folder_full_path)
    print(files)
    for file in files:
        if file == '.DS_Store':
            file_full_path = os.path.join(folder_full_path, file)
            print(file_full_path)
            os.remove(file_full_path)
            print(f"File [{file_full_path}] is deleted!")
            print()
