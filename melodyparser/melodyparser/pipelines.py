# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
import re

class MelodyparserPipeline:
    def process_item(self, item, spider):
        return item

class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield Request(image_url, meta={'title': item['title']})

    def file_path(self, request, response=None, info=None, *, item=None):
        # Извлекаем название карточки
        title = request.meta.get('title', 'default')
        title = re.sub(r'[^\w\-_\. ]', '_', title)  # удаляем опасные символы

        # Имя файла
        image_guid = os.path.basename(request.url)
        return f"{title}/{image_guid}"