from yandex_music import Client

yandex_music_client = Client().init()

search_result = yandex_music_client.search("Алиса в стране чудес 1976")

best_type = search_result.best.type
best_result = search_result.best.result

print(best_type)
print(best_result)

print(best_result.get_cover_url())