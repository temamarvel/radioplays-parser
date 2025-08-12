import os

import discogs_client
from dotenv import load_dotenv
from colored import Fore, Back, Style

load_dotenv()

DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

folders = sorted(os.listdir(ORGANIZED_PATH))

diskogs = discogs_client.Client('ExampleApplication/0.1', user_token=DISKOGS_TOKEN)

def get_diskogs_release(query):
    release = diskogs.search(query, type='master')
    return release.page(1)[0]

def remove_brackets(name: str):
    return name.split('[')[0]

# page = get_diskogs_release("Алиса в стране чудес")

for folder in folders:
    folder_path = os.path.join(ORGANIZED_PATH, folder)
    if not os.path.isdir(folder_path):
        continue

    name = remove_brackets(folder)
    try:
        master_release = get_diskogs_release(name)
        if master_release:
            print(f"{Fore.green} The {folder} has master release!{Style.reset}")
        else:
            print(f"{Fore.red} The {folder} doesn't have master release!{Style.reset}")
    except:
        print(f"{Fore.red}ERROR! Something goes wrong during the {folder} get master release info!{Style.reset}")
# print(page.title)
# print(page.year)