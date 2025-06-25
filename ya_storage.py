import os
import boto3
from dotenv import load_dotenv

load_dotenv()

YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

def get_s3_client():
    session = boto3.session.Session(aws_access_key_id=YANDEX_KEY_ID, aws_secret_access_key=YANDEX_KEY_SECRET)
    return session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")

# s3_client = get_s3_client()


LIMIT = 15
count = 0

def scan_folder(path: str, items):
    global count
    for item in items:
        if count == LIMIT:
            break

        item_path = os.path.join(path, item)

        if not os.path.isdir(item_path):
            print(item_path)
            count += 1
            continue

        subitems = os.listdir(item_path)
        scan_folder(item_path, subitems)


root_folders = sorted(os.listdir(ORGANIZED_PATH))

scan_folder(ORGANIZED_PATH, root_folders)

# s3_client.put_object(Bucket=YANDEX_BUCKET, Key='test/object_name', Body='TEST')
# s3_client.put_object(Bucket=YANDEX_BUCKET, Key='test/object_name/test3', Body='TEST')

#s3_client.upload_file('123.mp3', YANDEX_BUCKET, '123.mp3')

# for key in s3_client.list_objects(Bucket=YANDEX_BUCKET)['Contents']:
#     print(key['Key'])

# s3_client.upload_file(
#             fullname,
#             YANDEX_BUCKET,
#             ru_filename,
#         )