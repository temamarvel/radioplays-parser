import os
import json

ROOT_DIR = "audio/!ORGANIZED_AUDIO"

# Универсальная функция выбора нужных полей
def pick_fields(d: dict, keys: list[str]) -> dict:
    return {k: d[k] for k in keys if k in d}

def process_diskogs_release(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {"title": data.get("title"),
              "released": data.get("released"),
              "credits": [
                    pick_fields(artist, ["anv", "role"])
                    for artist in data.get("extraartists", [])
                    if any(k in artist for k in ("anv", "role"))
              ]
    }

    alt_cover = None
    images = []
    for img in data.get("images", []):
        simplified = pick_fields(img, ["type", "uri", "uri150"])
        if img.get("type") == "primary" and not alt_cover:
            alt_cover = simplified
        else:
            images.append(simplified)
    result["alt_cover"] = alt_cover
    result["images"] = images

    return result

def process_melodyinfo(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        fields = pick_fields(data, ["линки", "дополнительное описание"])
        return {
            "links": fields.get("линки"),
            "description": fields.get("дополнительное описание")
        }
    except Exception as e:
        print(f"⚠️ Не удалось прочитать melodyinfo.json: {e}")
        return {}

for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    if "diskogs_release.json" in filenames:
        diskogs_path = os.path.join(dirpath, "diskogs_release.json")
        melodyinfo_path = os.path.join(dirpath, "melodyinfo.json")
        output_path = os.path.join(dirpath, "data.json")

        try:
            base = process_diskogs_release(diskogs_path)
            if os.path.isfile(melodyinfo_path):
                base.update(process_melodyinfo(melodyinfo_path))
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(base, out, ensure_ascii=False, indent=2)
            print(f"✅ Сохранён data.json в {dirpath}")
        except Exception as e:
            print(f"❌ Ошибка в {dirpath}: {e}")