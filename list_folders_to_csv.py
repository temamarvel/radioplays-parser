import os
import csv

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"
IMAGES = "melodyparser/images"

def save_subfolders_to_csv(base_path: str, output_file: str = "folders_list.csv"):
    """
    Получает список подпапок в указанной папке и сохраняет их в CSV.

    :param base_path: Путь к исходной папке
    :param output_file: Имя выходного CSV-файла (по умолчанию folders_list.csv)
    """
    # Проверка на существование папки
    if not os.path.isdir(base_path):
        raise ValueError(f"Путь {base_path} не является папкой или не существует.")

    # Получаем список только подпапок (только 1 уровень вложенности)
    folders = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

    # Путь к CSV файлу
    csv_path = os.path.join(base_path, output_file)

    # Записываем в CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["#", "Название папки"])  # заголовки

        for i, folder in enumerate(folders, start=1):
            writer.writerow([i, folder])

    print(f"CSV файл сохранен: {csv_path}")

# Пример использования:
save_subfolders_to_csv(ORGANIZED_PATH, "organize.csv")
save_subfolders_to_csv(IMAGES, "melody.csv")