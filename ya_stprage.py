import os
import boto3

YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")

def get_s3_client():
    session = boto3.session.Session(
        aws_access_key_id=YANDEX_KEY_ID, aws_secret_access_key=YANDEX_KEY_SECRET
    )
    return session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

s3_client = get_s3_client()

# s3_client.put_object(Bucket=YANDEX_BUCKET, Key='object_name', Body='TEST')

#s3_client.upload_file('123.mp3', YANDEX_BUCKET, '123.mp3')

for key in s3_client.list_objects(Bucket=YANDEX_BUCKET)['Contents']:
    print(key['Key'])

# s3_client.upload_file(
#             fullname,
#             YANDEX_BUCKET,
#             ru_filename,
#         )