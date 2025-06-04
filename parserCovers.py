from bs4 import BeautifulSoup
import requests
import os
from colored import Fore, Back, Style
from downloader import download_file
import math

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


def download_cover_image(url, audio_name, name):
    local_folder_path = f"{save_folder}{audio_name}"
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    local_file_name = f"{local_folder_path}/{name}"
    if os.path.exists(local_file_name):
        print(f"{Fore.yellow}The file exists: {Style.bold}{local_file_name}{Style.reset}")
        return

    print(f"{Fore.yellow}Start download file: {Style.bold}{local_file_name}{Style.reset}")
    if download_file(f"{root_url}{url}{name}", local_file_name):
        print(f"\t{Fore.green}Success! The file is successfully downloaded{Style.reset}")
        # uncomment when you need to log downloaded files
        # downloaded_audio.update({f"{url}{name}": filename})
    else:
        print(f"\t{Fore.red}Error! Something wrong with file downloading{Style.reset}")


def scan_folder_for_audio(url):
    full_url = f"{root_url}{url}"

    bs = get_parsed_soup(full_url)

    for link in bs.find_all('a'):
        name = link.get('href')

        if is_trash_link(name):
            continue

        path = os.path.splitext(name)
        filename = path[0]
        ext = path[1]

        new_url = f"{url}{name}"

        if ext == '.mp3':
            scan_folder_for_covers(url, name)

        if ext != '':
            continue

        scan_folder_for_audio(new_url)

def scan_folder_for_covers(url, audio_name):
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

        if ext == '.jpeg' or ext == '.jpg' or ext == '.bmp' or ext == '.png':
            mp3count += 1
            download_cover_image(url, audio_name, name)

        if ext != '':
            continue

DOWNLOADS_LIMIT = 3

root_url = 'http://audio.arjlover.net/audio/'
save_folder = "audio/!COVERS/"

print(f"{Fore.yellow}== START =={Style.reset}")
print(f"{Fore.yellow}== Parse album cover images files from {root_url} =={Style.reset}")
print()

# uncomment when you need to log downloaded files
# downloaded_audio = dict()

root_folders = {}

get_root_folders(root_url)

downloads_count = 0
root_folders_count = len(root_folders)

for folder_url in root_folders.keys():
    if downloads_count == DOWNLOADS_LIMIT:
        break
    downloads_count += 1
    print(f"{Style.bold}{Fore.blue}[{downloads_count} / {root_folders_count} ] {math.ceil(downloads_count / (root_folders_count / 100))}% complete {Style.reset}")
    scan_folder_for_audio(folder_url)

print()
print(f"{Fore.yellow}== END =={Style.reset}")
