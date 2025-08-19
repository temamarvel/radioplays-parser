import os

import discogs_client
from dotenv import load_dotenv
from colored import Fore, Back, Style

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

for folder in folders:
    folder_path = os.path.join(ORGANIZED_PATH, folder)
    if not os.path.isdir(folder_path):
        continue

    name = remove_brackets(folder)
    try:
        master_release = get_diskogs_release(name, 'master')
        if master_release:
            print(f"{Fore.green} The {folder} has MASTER RELEASE!{Style.reset}")
            continue
        else:
            print(f"{Fore.red} The {folder} doesn't have MASTER RELEASE!{Style.reset}")

        release = get_diskogs_release(name, 'release')
        if release:
            print(f"{Fore.green} The {folder} has RELEASE!{Style.reset}")
            continue
        else:
            print(f"{Fore.red} The {folder} doesn't have RELEASE!{Style.reset}")
    except Exception as e:
        print(f"{Fore.red}ERROR! {e} Something goes wrong during the {folder} get release info!{Style.reset}")
# print(page.title)
# print(page.year)