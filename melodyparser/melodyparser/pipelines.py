# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import os
import re
import hashlib
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

WS_RE = re.compile(r'\s+')

def slugify(s: str) -> str:
    if not s:
        return "untitled"
    s = s.replace('\xa0', ' ')
    s = WS_RE.sub(' ', s).strip()
    # безопасное имя папки: буквы/цифры/пробел/._-
    s = re.sub(r'[^\w\-. ]+', '_', s)
    return s[:120] or "untitled"

class MelodyparserPipeline:
    def process_item(self, item, spider):
        return item

class MyImagePipeline(ImagesPipeline):
    """
    Сохраняет изображения в IMAGES_STORE/<folder>/...
    И пишет рядом IMAGES_STORE/<folder>/metadata.json
    """

    def get_media_requests(self, item, info):
        # Можно проставить заголовки/реферер, если нужно
        for url in item.get('image_urls', []):
            yield Request(url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Имя папки: приоритет — folder_hint, иначе title
        folder = slugify(item.get('folder_hint') or item.get('title'))
        # Имя файла: стараемся взять имя из URL, иначе sha1 + .jpg
        path = urlparse(request.url).path
        name = os.path.basename(path)
        root, ext = os.path.splitext(name)
        if not ext:
            ext = ".jpg"
        if not root:
            root = hashlib.sha1(request.url.encode()).hexdigest()
        filename = root + ext
        return f"{folder}/{filename}"

    def item_completed(self, results, item, info):
        # results -> [(ok, {'path': 'folder/file.jpg', 'checksum': '...'}), ...]
        image_paths = [r['path'] for ok, r in results if ok]
        item['images'] = image_paths

        # Абсолютный путь до папки карточки
        folder = slugify(item.get('folder_hint') or item.get('title'))
        # Filesystem backend: получить корень стора
        # В разных версиях Scrapy store реализован чуть иначе:
        try:
            base_dir = self.store._get_filesystem_path('')  # >=2.7
        except Exception:
            base_dir = getattr(self.store, 'basedir', None) or self.store.root_dir
        out_dir = os.path.join(base_dir, folder)
        os.makedirs(out_dir, exist_ok=True)

        # Собираем JSON
        meta = {
            "url": item.get('url'),
            "title": item.get('title'),
            "record": item.get('date_of_record'),
            "release": item.get('release'),
            "props_text": item.get('props_text'),
            "links": item.get('links'),
            # "credits": item.get('credits'),
            # "cast": item.get('cast'),
            "description": item.get('description'),
            "images": [os.path.basename(p) for p in image_paths],
        }

        out_path = os.path.join(out_dir, "metadata.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        # Вернём item (Scrapy может ещё другие пайплайны прогнать)
        return item
    # def get_media_requests(self, item, info):
    #     for image_url in item.get('image_urls', []):
    #         yield Request(image_url, meta={'title': item['title']})
    #
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     # Извлекаем название карточки
    #     title = request.meta.get('title', 'default')
    #     title = re.sub(r'[^\w\-_\. ]', '_', title)  # удаляем опасные символы
    #
    #     # Имя файла
    #     _, ext = os.path.splitext(request.url)
    #     return f"{title}/{title}_main{ext}"