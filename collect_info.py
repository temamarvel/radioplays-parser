import os
import json

ROOT_DIR = "audio/!ORGANIZED_AUDIO"

def pick_fields(d: dict, keys: list[str]) -> dict:
    return {k: d[k] for k in keys if k in d}

def process_diskogs_release(json_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title")
    released = data.get("released")

    simplified_artists = [
        pick_fields(extraartist, ["anv", "role"])
        for extraartist in data.get("extraartists", [])
    ]

    alt_cover = None
    images = []

    for img in data.get("images", []):
        simplified = pick_fields(img, ["type", "uri", "uri150"])
        if img.get("type") == "primary" and not alt_cover:
            alt_cover = simplified
        else:
            images.append(simplified)

    return {
        "title": title,
        "released": released,
        "extraartists": simplified_artists,
        "alt_cover": alt_cover,
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