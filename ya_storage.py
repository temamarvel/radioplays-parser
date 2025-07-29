import mimetypes
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

allowed_file_ext = [".mp3", ".webp"]

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


LIMIT = 20
count = 0

def remove_brackets(name: str):
    return name.split('[')[0]

def scan_folder(path: str, items):
    global count
    for item in items:
        if count == LIMIT:
            break

        item_path = os.path.join(path, item)

        if (not path) and os.path.isdir(item_path):
            print()
            name = item
            title = remove_brackets(name)
            new_play = Play(title=title, name=name, s3_folder_key=item_path)
            # if not is_play_in_database(new_play):
            #     add_item_to_database(new_play)
            add_item_to_database(new_play)

        if not os.path.isdir(item_path):
            print(f"{Fore.blue}{item_path}{Style.reset}")

            name, ext = os.path.splitext(item_path)
            if not ext in allowed_file_ext:
                print(f"{Fore.yellow}The file {item_path} extension isn't allowed to upload to s3. The file skipped!{Style.reset}")
                continue



            # todo uncomment for upload
            # if not is_item_uploaded(item_path):
            #     content_type, _ = mimetypes.guess_type(item_path)
            #     if content_type is None:
            #         content_type = "application/octet-stream"
            #
            #     s3_client.upload_file(item_path, YANDEX_BUCKET, item_path, ExtraArgs={"ContentType": content_type})
            #     print(f"{Fore.green}The file {Style.bold}[{item_path}]{Style.reset}{Fore.yellow} is uploaded to the bucket.{Style.reset}")
            #
            # count += 1
            # continue

        if os.path.isdir(item_path):
            subitems = os.listdir(item_path)
            scan_folder(item_path, subitems)

os.chdir(ORGANIZED_PATH)

root_folders = sorted(os.listdir())

s3_client = get_s3_client()

scan_folder("", root_folders)