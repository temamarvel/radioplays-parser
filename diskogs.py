import os
import discogs_client

DISKOGS_TOKEN = os.getenv("DISKOGS_TOKEN")

diskogs = discogs_client.Client('ExampleApplication/0.1', user_token=DISKOGS_TOKEN)



def get_dickogs_release_url():
    release = diskogs.search('Queen II', type='release')
    page = release.page(1)[0]
    url = page.url
    print(url)
    return url