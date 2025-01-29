from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

root_url = 'http://audio.arjlover.net/audio/'

print("===================")

count = 0

def scan_folder(url, level):
    response = requests.get(url)

    if response.status_code != 200:
        return

    bs = BeautifulSoup(response.text, "html.parser")

    for link in bs.find_all('a'):
        name = link.get('href')
        if "?C" in name or "../" in name:
            continue

        path = os.path.splitext(name)
        ext = path[1]
        filename = path[0]
        print('\t' * level + name)
        if ext != '':
            continue
        new_url = f"{url}{name}"
        scan_folder(new_url, level + 1)