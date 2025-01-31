from bs4 import BeautifulSoup
import requests
import os
from colored import Fore, Back, Style
import re

root_url = 'http://audio.arjlover.net/audio/'
save_folder = "audio/"

print(f"{Fore.green}==================={Style.reset}")

dictionary = dict()

root_folders = dict()

count = 0


def get_root_folders(url):
    response = requests.get(url)

    if response.status_code != 200:
        return

    bs = BeautifulSoup(response.text, "html.parser")

    for link in bs.find_all('a'):
        if count == 500:
            return
        name = link.get('href')
        if "?C" in name or "../" in name or not name.endswith('/'):
            continue

        root_folders.update({name: 0})


def scan_folder(url, level):
    # print(url)

    response = requests.get(url)

    if response.status_code != 200:
        return 0

    bs = BeautifulSoup(response.text, "html.parser")

    # links = bs.find_all('a')
    # print(links.__len__())

    mp3count = 0

    for link in bs.find_all('a'):
        name = link.get('href')
        if "?C" in name or "../" in name:
            continue

        path = os.path.splitext(name)
        ext = path[1]
        filename = path[0]
        # print('\t' * level + name)
        if ext == '.mp3':
            mp3count += 1
            short_url = url.replace(root_url, "")

            folder_path = f"{save_folder}{short_url}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            dictionary.update({f"{short_url}{name}": filename})
        if ext != '':
            continue
        new_url = f"{url}{name}"
        mp3count += scan_folder(new_url, level + 1)

    return mp3count


get_root_folders(root_url)

# for key, value in root_folders.items():
#     print(f"{key} : {value}")


for folder_url in root_folders.keys():
    count += 1
    if count == 10:
        break
    root_folders[folder_url] = scan_folder(f"{root_url}{folder_url}", 1)

# scan_folder(root_url, 0)
print(f"{Fore.green}===================")
print("end scan")
print(f"==================={Style.reset}")

RE_D = re.compile('\d')


def has_nums(string):
    return RE_D.search(string)


# for key, value in dictionary.items():
#     if has_nums(value):
#         print(f"{Fore.red}{key} : {value}{Style.reset}")
#     else:
#         print(f"{Fore.green}{key} : {value}{Style.reset}")

print(f"{Fore.green}===================")
print("mp3 counts")
print(f"==================={Style.reset}")

good_count = 0
bad_count = 0
for key, value in root_folders.items():
    if value == 1:
        good_count += 1
        print(f"{Fore.green}{key} : {value}{Style.reset}")
    else:
        bad_count += 1
        print(f"{Fore.red}{key} : {value}{Style.reset}")

print(f"good_count = {good_count}")
print(f"bad_count = {bad_count}")
# print(f"{key} : {value}")
