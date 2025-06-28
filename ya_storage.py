import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from colored import Fore, Back, Style

from db_Alchemy import add_item_to_database, is_play_in_database
from db_models import Play

load_dotenv()

YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")

ORGANIZED_PATH = "audio/!ORGANIZED_AUDIO"

def get_s3_client():
    session = boto3.session.Session(aws_access_key_id=YANDEX_KEY_ID, aws_secret_access_key=YANDEX_KEY_SECRET)
    return session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")

def is_item_uploaded(s3_key):
    try:
        s3_client.head_object(Bucket=YANDEX_BUCKET, Key=s3_key)
        print(f"{Fore.green}The file {Style.bold}[{s3_key}]{Style.reset}{Fore.green} is existed in the bucket.{Style.reset}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"{Fore.yellow}The file {Style.bold}[{s3_key}]{Style.reset}{Fore.yellow} isn't existed in the bucket.{Style.reset}")
        else:
            print(f"{Fore.red}Error: {e}{Style.reset}")
    return False


LIMIT = 15
count = 0

def scan_folder(path: str, items):
    global count
    for item in items:
        if count == LIMIT:
            break

        item_path = os.path.join(path, item)

        if (not path) and os.path.isdir(item_path):
            print()
            new_play = Play(name=item, s3_folder_key=item_path)
            if not is_play_in_database(new_play):
                add_item_to_database(new_play)

        if not os.path.isdir(item_path):
            print(f"{Fore.blue}{item_path}{Style.reset}")

            # todo uncomment for upload
            # if not is_item_uploaded(item_path):
            #     s3_client.upload_file(item_path, YANDEX_BUCKET, item_path)

            count += 1
            continue

        subitems = os.listdir(item_path)
        scan_folder(item_path, subitems)

os.chdir(ORGANIZED_PATH)

root_folders = sorted(os.listdir())

s3_client = get_s3_client()

scan_folder("", root_folders)