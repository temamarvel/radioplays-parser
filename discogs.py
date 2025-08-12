import os
import discogs_client
from dotenv import load_dotenv

load_dotenv()

DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

diskogs = discogs_client.Client('ExampleApplication/0.1', user_token=DISKOGS_TOKEN)

def get_diskogs_release(query):
    release = diskogs.search(query, type='master')
    return release.page(1)[0]


page = get_diskogs_release("Алиса в стране чудес")

print(page.title)
print(page.year)