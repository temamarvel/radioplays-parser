import os

import discogs_client
from dotenv import load_dotenv
from colored import Fore, Back, Style
import json

load_dotenv()

DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

folders = sorted(os.listdir(ORGANIZED_PATH))

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

def save_to_file(data, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"{Fore.yellow} The release saved to {path}!{Style.reset}")

for folder in folders:
    folder_path = os.path.join(ORGANIZED_PATH, folder)
    if not os.path.isdir(folder_path):
        continue

    name = remove_brackets(folder)
    try:
        master_release = get_diskogs_release(name, 'master')
        if master_release:
            print(f"{Fore.green} The {folder} has MASTER RELEASE!{Style.reset}")
            master_release.refresh()
            save_to_file(master_release.data, os.path.join(folder_path, "diskogs_master.json"))
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
            save_to_file(release.data, os.path.join(folder_path, "diskogs_release.json"))
            continue
        else:
            print(f"{Fore.red} The {folder} doesn't have RELEASE!{Style.reset}")
    except Exception as e:
        print(f"{Fore.red}ERROR! {e} Something goes wrong during the {folder} get release info!{Style.reset}")
# print(page.title)
# print(page.year)