# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MelodyparserItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()  # для ImagesPipeline (вход)
    images = scrapy.Field()      # сюда Scrapy положит инфо о скачанных файлах (выход)
    date_of_record = scrapy.Field()
    links = scrapy.Field()
    description = scrapy.Field()
    # credits = scrapy.Field()
    # cast = scrapy.Field()
    folder_hint = scrapy.Field()  # опционально: имя папки (каталожный № и т.п.)
