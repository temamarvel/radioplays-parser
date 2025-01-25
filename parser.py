from bs4 import BeautifulSoup
import requests
import os
from yandex_cloud_ml_sdk import  YCloudML
import boto3
from botocore.config import Config
import discogs_client
from dotenv import load_dotenv

load_dotenv()

url = 'http://audio.arjlover.net/audio/Volk_i_Semero_Kozliat_na_novii_lad/'

YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")
YANDEX_ML_FOLDER_ID = os.getenv("YANDEX_ML_FOLDER_ID")
YANDEX_ML_KEY_SECRET = os.getenv("YANDEX_ML_KEY_SECRET")
DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

response = requests.get(url)

print(response)

bs = BeautifulSoup(response.text, "html.parser")

print(response.text)
print("===================")
print(bs)

def get_s3_client():
    session = boto3.session.Session(
        aws_access_key_id=YANDEX_KEY_ID, aws_secret_access_key=YANDEX_KEY_SECRET
    )
    return session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )


def download_file(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Open the local file to write the downloaded content
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

print("===================")


sdk = YCloudML(
        folder_id=YANDEX_ML_FOLDER_ID,
        auth=YANDEX_ML_KEY_SECRET,
    )

s3_client = get_s3_client()

# s3_client.put_object(Bucket=YANDEX_BUCKET, Key='object_name', Body='TEST')

#s3_client.upload_file('123.mp3', YANDEX_BUCKET, '123.mp3')

d = discogs_client.Client('ExampleApplication/0.1', user_token=DISKOGS_TOKEN)

res = d.search('Queen II', type='release')

p = res.page(1)[0]
u = p.url
t = p.thumb
print(u)

print(res.page(1))

print("uploaded")

# for link in bs.find_all('a'):
#     name = link.get('href')
#     path = os.path.splitext(name)
#     ext = path[1]
#     filename = path[0]
#
#
#
#     messages = [
#         {
#             "role": "system",
#             "text": "Транслитерируй на русский, результат запиши без кавычек, в качестве разделителя между словами используй одинарный пробел вместо нижнего подчеркивания",
#         },
#
#         {
#             "role": "user",
#             "text": f"{filename}",
#         },
#     ]
#
#     if ext == ".mp3":
#         result = (
#             sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)
#         )
#
#         ru_filename = result[0].text
#         fullname = f"{ru_filename}{ext}"
#
#         # download_file(f"{url}{name}", fullname)
#
#         # s3_client.upload_file(
#         #     fullname,
#         #     YANDEX_BUCKET,
#         #     ru_filename,
#         # )
#
#         print(ru_filename)
#
#     if ext == ".jpeg" or ext == ".jpg":
#         print(name)
#         download_file(f"{url}{name}", name)

for key in s3_client.list_objects(Bucket=YANDEX_BUCKET)['Contents']:
    print(key['Key'])