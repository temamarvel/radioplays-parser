import scrapy


class MelodyspiderSpider(scrapy.Spider):
    name = "melodyspider"
    allowed_domains = ["melody.su"]
    start_urls = ["https://melody.su/catalog/children/"]

    def parse(self, response):
        # 1. Находим карточки
        cards = response.css("div.entity-snippet a::attr(href)").get()
        for card_url in cards:
            full_url = response.urljoin(card_url)
            yield scrapy.Request(full_url, callback=self.parse_detail)

        # 2. Переход на следующую страницу
        # next_page = response.css("li.pagination__item_type_next a::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        # Парсим детальную информацию
        yield {
            "title": response.css("h1::text").get(),
            "text": response.css("div.content p::text").getall(),
            "images": response.css("img::attr(src)").getall(),
            "links": response.css("a::attr(href)").getall()
        }
