from bs4 import BeautifulSoup
import requests
import os
from colored import Fore, Back, Style
from downloader import download_file


DOWNLOADS_LIMIT = 3


root_url = 'http://audio.arjlover.net/audio/'
save_folder = "audio/"


print(f"{Fore.yellow}== START =={Style.reset}")
print(f"{Fore.yellow}== Parse audio files from {root_url} =={Style.reset}")
print()

# uncomment when you need to log downloaded files
# downloaded_audio = dict()

root_folders = dict()


def get_parsed_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        return

    return BeautifulSoup(response.text, "html.parser")


def is_trash_link(ref_name):
    return "?C" in ref_name or "../" in ref_name


def get_root_folders(url):
    bs = get_parsed_soup(url)

    for link in bs.find_all('a'):
        name = link.get('href')
        if is_trash_link(name) or not name.endswith('/'):
            continue

        root_folders.update({name: 0})

def download_audio(url, name):
    local_folder_path = f"{save_folder}{url}"
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    local_file_name = f"{local_folder_path}{name}"
    print(f"{Fore.yellow}Start download file: {Style.bold}{local_file_name}{Style.reset}")
    if download_file(f"{root_url}{url}{name}", local_file_name):
        print(f"\t{Fore.green}The file is successfully downloaded{Style.reset}")
        # uncomment when you need to log downloaded files
        # downloaded_audio.update({f"{url}{name}": filename})
    else:
        print(f"\t{Fore.red}Something wrong with file downloading{Style.reset}")

def scan_folder(url):
    full_url = f"{root_url}{url}"

    bs = get_parsed_soup(full_url)

    mp3count = 0

    for link in bs.find_all('a'):
        name = link.get('href')

        if is_trash_link(name):
            continue

        path = os.path.splitext(name)
        filename = path[0]
        ext = path[1]

        new_url = f"{url}{name}"

        if ext == '.mp3':
            mp3count += 1
            download_audio(url, name)

        if ext != '':
            continue

        mp3count += scan_folder(new_url)

    return mp3count


get_root_folders(root_url)

downloads_count = 0

for folder_url in root_folders.keys():
    if downloads_count == DOWNLOADS_LIMIT:
        break
    downloads_count += 1
    root_folders[folder_url] = scan_folder(folder_url)


print()
print(f"{Fore.yellow}===================")
print("MP3 COUNTS")
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

print()
print(f"{Fore.green}good_count = {good_count}{Style.reset}")
print(f"{Fore.red}bad_count = {bad_count}{Style.reset}")

print()
print(f"{Fore.yellow}== END =={Style.reset}")
