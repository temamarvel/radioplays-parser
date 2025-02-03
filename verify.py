import os

root_path = "audio/"
os.chdir(root_path)

folders = os.listdir()

print(folders)

for folder in folders:
    if not os.path.isdir(f"{folder}"):
        continue
    subfolders = os.listdir(f"{folder}")
    filtered_folder = filter(lambda x: os.path.isdir(os.path.join(folder,x)) , subfolders)
    filtered_mp3 = filter(lambda x: os.path.isdir(os.path.join(folder, x)), subfolders)
    print(subfolders)
    print(list(filtered_folder))