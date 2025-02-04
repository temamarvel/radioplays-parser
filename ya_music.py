from yandex_music import Client
from discogs import get_diskogs_release

yandex_music_client = Client().init()

release = get_diskogs_release("Алиса в стране чудес")

search_result = yandex_music_client.search(f"{release.title} {release.year}")

best_type = search_result.best.type
best_result = search_result.best.result

# print(best_type)
# print(best_result)

print(best_result.get_cover_url())
id = best_result.id
print(id)
print(f"https://music.yandex.ru/album/{id}")