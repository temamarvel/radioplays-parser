import os
import json
from colored import Fore, Back, Style

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
TRACKS_JSON_PATH = os.path.join(ORGANIZED_PATH, "записи_с_линками.json")


ROOT_DIR = ORGANIZED_PATH


with open(TRACKS_JSON_PATH, "r", encoding="utf-8") as f:
    tracks = json.load(f)


track_by_title = {t["название"]: t for t in tracks}


for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    print(f"{Fore.blue}-- {dirpath} --{Style.reset}")
    if "metadata.json" in filenames:
        metadata_path = os.path.join(dirpath, "metadata.json")
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"{Fore.red}Ошибка при чтении {metadata_path}: {e}{Style.reset}")
            continue

        title = metadata.get("title")
        if title in track_by_title:
            output_path = os.path.join(dirpath, "melodyinfo.json")
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(track_by_title[title], out, ensure_ascii=False, indent=2)
            print(f"{Fore.green}Создан melodyinfo.json для: {title}{Style.reset}")
        else:
            print(f"{Fore.red}Не найден трек для: {title}{Style.reset}")