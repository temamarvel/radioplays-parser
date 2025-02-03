import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import  YCloudML

load_dotenv()

YANDEX_ML_FOLDER_ID = os.getenv("YANDEX_ML_FOLDER_ID")
YANDEX_ML_KEY_SECRET = os.getenv("YANDEX_ML_KEY_SECRET")

sdk = YCloudML(
        folder_id=YANDEX_ML_FOLDER_ID,
        auth=YANDEX_ML_KEY_SECRET,
    )

def translate_to_russian(name):
    path = os.path.splitext(name)
    ext = path[1]
    filename = path[0]

    messages = [
        {
            "role": "system",
            "text": "Транслитерируй на русский, результат запиши без кавычек, в качестве разделителя между словами используй одинарный пробел вместо нижнего подчеркивания",
        },

        {
            "role": "user",
            "text": f"{filename}",
        },
    ]

    if ext == ".mp3":
        result = (sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages))

    ru_filename = result[0].text
    ru_fullname = f"{ru_filename}{ext}"

    print(ru_filename)
    return ru_fullname
#
#     ru_filename = result[0].text
#     fullname = f"{ru_filename}{ext}"
#
#     # download_file(f"{url}{name}", fullname)
#
#     # s3_client.upload_file(
#     #     fullname,
#     #     YANDEX_BUCKET,
#     #     ru_filename,
#     # )
#