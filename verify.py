import os

root_path = "audio/"

folders = os.listdir(root_path)

print(folders)

for folder in folders:
    if not os.path.isdir(f"{root_path}{folder}"):
        continue
    subfolders = os.listdir(f"{root_path}{folder}")
    filtered_folder = filter(lambda x: os.path.isdir(os.path.join(root_path,folder,x)) , subfolders)
    filtered_mp3 = filter(lambda x: os.path.isdir(os.path.join(root_path, folder, x)), subfolders)
    print(subfolders)
    print(list(filtered_folder))

