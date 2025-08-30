import os.path
import unicodedata
from yandex_music import Client
# from discogs import get_diskogs_release
from colored import Fore, Back, Style
import json

# from playInfos_db import title

yandex_music_client = Client().init()


ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

# folders = [unicodedata.normalize("NFC", folder) for folder in sorted(os.listdir(ORGANIZED_PATH)) if os.path.isdir(folder)]

def remove_brackets(name: str):
    return name.split('[')[0]

folders = sorted(os.listdir(ORGANIZED_PATH))

for folder in folders:
    folder = unicodedata.normalize("NFC", folder)
    folder_path = os.path.join(ORGANIZED_PATH, folder)
    if not os.path.isdir(folder_path):
        continue

    ya_release = None

    json_path = os.path.join(folder_path, "data.json")
    if not os.path.exists(json_path):
        ya_release = yandex_music_client.search(remove_brackets(folder), type_= "track")
    else:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"{Fore.red}Ошибка при чтении {json_path}: {e}{Style.reset}")
            continue

        title = data.get("title")
        ya_release = yandex_music_client.search(title, type_= "track")

    if not ya_release.tracks:
        continue

    ya_release_best = ya_release.tracks.results[0]

    if not ya_release_best:
        continue

    ya_url = f"https://music.yandex.ru/album/{ya_release_best.albums[0].id}/track/{ya_release_best.id}"

    result = { "title": folder,
               "ya_title": ya_release_best.title,
               "ya_url": ya_url}

    output_path = os.path.join(folder_path, "ya_info.json")
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
    print(f"{Fore.blue}Folder = [{folder}] Ya_title = [{ya_release_best.title}]{Style.reset}")
    print(f"{Fore.green}Создан ya_info.json для: {folder}{Style.reset}")

# release = get_diskogs_release("Алиса в стране чудес")
#
# search_result = yandex_music_client.search(f"{release.title} {release.year}")
#
# best_type = search_result.best.type
# best_result = search_result.best.result
#
# # print(best_type)
# # print(best_result)
#
# print(best_result.get_cover_url())
# id = best_result.id
# print(id)
# print(f"https://music.yandex.ru/album/{id}")