import os
import json

ROOT_DIR = "audio/!ORGANIZED_AUDIO"

def process_diskogs_release(json_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title")
    released = data.get("released")
    images = data.get("images", [])
    extraartists = data.get("extraartists", [])

    simplified_artists = [
        {"anv": a.get("anv"), "role": a.get("role")}
        for a in extraartists if "anv" in a or "role" in a
    ]

    return {
        "title": title,
        "released": released,
        "extraartists": simplified_artists,
        "images": images
    }

for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    if "diskogs_release.json" in filenames:
        diskogs_path = os.path.join(dirpath, "diskogs_release.json")
        output_path = os.path.join(dirpath, "data.json")

        try:
            result = process_diskogs_release(diskogs_path)
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(result, out, ensure_ascii=False, indent=2)
            print(f"✅ Создан data.json в {dirpath}")
        except Exception as e:
            print(f"❌ Ошибка при обработке {diskogs_path}: {e}")