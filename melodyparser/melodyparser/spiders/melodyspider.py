import scrapy

from ..items import MelodyparserItem


class MelodyspiderSpider(scrapy.Spider):
    name = "melodyspider"
    allowed_domains = ["melody.su"]
    start_urls = ["https://melody.su/catalog/children/"]

    def parse(self, response):
        # 1. Находим карточки
        cards = response.css("div.entity-snippet a::attr(href)").get()
        print(f"!!cards!!={cards}")
        # for card_url in cards:
        #     full_url = response.urljoin(card_url)
        #     print(f"!!full_url!!={full_url}")
        #     yield scrapy.Request(full_url, callback=self.parse_detail)


        # todo make real parser
        # parse title, all info, download images aggregate it in one folder with title
        full_url = response.urljoin(cards)
        print(f"!!full_url!!={full_url}")
        yield scrapy.Request(full_url, callback=self.parse_detail)

        # 2. Переход на следующую страницу
        # next_page = response.css("li.pagination__item_type_next a::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = MelodyparserItem()
        item['title'] = response.css("h1::text").get()
        item['image_urls'] = response.css("div.gallery__slide img::attr(src)").getall()

        # если пути относительные — превратим в абсолютные
        item['image_urls'] = [response.urljoin(url) for url in item['image_urls']]

        yield item
        # Парсим детальную информацию
        # yield {
        #     "title": response.css("h1::text").get(),
        #     # "text": response.css("div.content p::text").getall(),
        #     "images": response.css("picture.gallery__picture img::attr(src)").getall(),
        #     # "links": response.css("a::attr(href)").getall()
        # }
