import os
import time
import unicodedata

import discogs_client
from dotenv import load_dotenv
from colored import Fore, Back, Style
import json

load_dotenv()

DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

row_folders = [unicodedata.normalize("NFC", folder) for folder in sorted(os.listdir(ORGANIZED_PATH))]

filtered_folders = [unicodedata.normalize("NFC", folder) for folder in row_folders if not os.path.isfile(os.path.join(ORGANIZED_PATH, folder, "diskogs_release.json"))]

diskogs = discogs_client.Client('ExampleApplication/0.1', user_token=DISKOGS_TOKEN)

def get_diskogs_release(query: str, release_type: str):
    release = diskogs.search(query, type=release_type)
    if release.page(1):
        return release.page(1)[0]
    else:
        return None


def remove_brackets(name: str):
    return name.split('[')[0]

# page = get_diskogs_release("Алиса в стране чудес")

def remove_old(folders: list[str]):
    for folder in folders:
        folder_path = os.path.join(ORGANIZED_PATH, folder)
        if not os.path.isdir(folder_path):
            continue
        master_path = os.path.join(folder_path, "diskogs_master.json")
        if os.path.exists(master_path):
            os.remove(master_path)
        release_path = os.path.join(folder_path, "diskogs_release.json")
        if os.path.exists(release_path):
            os.remove(release_path)

def save_to_file(data, path: str, name):
    with open(path, "w", encoding="utf-8") as f:
        title = data["title"]
        print(f"{Fore.yellow} The release title is {title}!{Style.reset}")
        if remove_brackets(name).lower() != title.lower():
            print(f"{Fore.red} NAME={name} != TITLE={title}!{Style.reset}")
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"{Fore.yellow} The release saved to {path}!{Style.reset}")

def request_to_diskogs(folders: list[str]):
    master_release_count = 0
    release_count = 0

    for folder in folders:
        folder_path = os.path.join(ORGANIZED_PATH, folder)
        if not os.path.isdir(folder_path):
            continue

        name = remove_brackets(folder).replace("Ё", "Е").replace("ё", "е")

        try:
            time.sleep(0.2)
            master_release = get_diskogs_release(name, 'master')
            if master_release:
                print(f"{Fore.green} The {folder} has MASTER RELEASE!{Style.reset}")
                master_release.refresh()
                save_to_file(master_release.data, os.path.join(folder_path, "diskogs_master.json"), folder)
                master_release_count += 1
            else:
                print(f"{Fore.red} The {folder} doesn't have MASTER RELEASE!{Style.reset}")

            release = None
            if master_release:
                release = master_release.main_release
            else:
                release = get_diskogs_release(name, 'release')
            if release:
                print(f"{Fore.green} The {folder} has RELEASE!{Style.reset}")
                release.refresh()
                save_to_file(release.data, os.path.join(folder_path, "diskogs_release.json"), folder)
                release_count += 1
                continue
            else:
                print(f"{Fore.red} The {folder} doesn't have RELEASE!{Style.reset}")
        except Exception as e:
            print(f"{Fore.red}ERROR! {e} Something goes wrong during the {folder} get release info!{Style.reset}")

    print(f"{Fore.blue}MASTER RELEASES count = {master_release_count}{Style.reset}")
    print(f"{Fore.blue}RELEASES count = {release_count}{Style.reset}")

remove_old(row_folders)

request_to_diskogs(row_folders)



# print(page.title)
# print(page.year)