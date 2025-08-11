import scrapy

from ..items import MelodyparserItem


import re
from urllib.parse import urljoin

WS_RE = re.compile(r'\s+')
DASH_SPLIT_RE = re.compile(r'\s*[—\-:]\s*')  # разделители: —  -  :

def clean_text(s):
    if not s:
        return None
    s = s.replace('\xa0', ' ')
    s = WS_RE.sub(' ', s).strip()
    return s or None

def get_paragraph_lines(p_sel):
    # забираем ВСЕ текстовые узлы из <p>, чистим и фильтруем пустое
    lines = [clean_text(t) for t in p_sel.xpath('.//text()').getall()]
    return [ln for ln in lines if ln]

def parse_credits(lines):
    """
    строки вида:
      'Инсценировка Александр ...'
      'Музыка Андрей ...'
      'Режиссер — Александр Вилькин'
      'Феликс Зальтен, перевод Юрия Нагибина'  (без явного разделителя)
    превращаем в список словарей с 1 ключом.
    """
    out = []
    for ln in lines:
        # 1) сначала пробуем разделить по — / - / :
        parts = DASH_SPLIT_RE.split(ln, 1)
        if len(parts) == 2:
            key = clean_text(parts[0].rstrip(':'))
            val = clean_text(parts[1])
            if key and val:
                out.append({key: val})
                continue

        # 2) эвристики для частых случаев без разделителя
        low = ln.lower()
        if "перевод" in low and "," in ln:
            # "Феликс Зальтен, перевод Юрия Нагибина"
            out.append({"Автор/перевод": ln})
        else:
            # fallback — просто как примечание
            out.append({"Примечание": ln})
    return out

def parse_cast(lines):
    """
    строки вида:
      'Бемби — Вера Чернявская'
      'Листья — Галина Широкова, Владимир Гинзбург'
    → [{'Бемби': 'Вера Чернявская'}, {'Листья':'Галина Широкова, Владимир Гинзбург'}]
    """
    out = []
    for ln in lines:
        parts = DASH_SPLIT_RE.split(ln, 1)
        if len(parts) == 2:
            role = clean_text(parts[0])
            actors = clean_text(parts[1])
            if role and actors:
                # если несколько исполнителей через запятую — оставим как одну строку
                out.append({role: actors})
        else:
            # строка без разделителя — как примечание
            out.append({"Примечание": ln})
    return out

def extract_music_links(props_container_sel, base_url):
    """
    В твоей разметке музыкальные ссылки лежат внутри одного из .props__prop,
    где label пустой, а в value — несколько <a>.
    Соберём их в нужном формате.
    """
    links = []
    for block in props_container_sel.css(".props__prop"):
        label_text = clean_text(block.css(".props__label::text").get())
        a_tags = block.css(".props__value a")
        if not a_tags:
            continue
        # если в блоке есть <a>, забираем как музыкальные ссылки
        for a in a_tags:
            href = a.attrib.get("href")
            if not href:
                continue
            links.append({
                "text": clean_text(a.css("::text").get()),
                "href": urljoin(base_url, href),
                "target": a.attrib.get("target")
            })
    return links or None


class MelodyspiderSpider(scrapy.Spider):
    name = "melodyspider"
    allowed_domains = ["melody.su"]
    start_urls = ["https://melody.su/catalog/children/"]

    def parse(self, response):
        # 1. Находим карточки
        cards = response.css("div.entity-snippet a.entity-snippet__illustration::attr(href)").getall()
        print(f"!!cards!!={cards}")
        for card_url in cards:
            full_url = response.urljoin(card_url)
            print(f"!!full_url!!={full_url}")
            yield scrapy.Request(full_url, callback=self.parse_detail)


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
        item['url'] = response.url
        item['title'] = response.css("h1::text").get()

        # картинки
        item['image_urls'] = response.css("div.gallery__slide img::attr(src)").getall()
        item['image_urls'] = [response.urljoin(u) for u in item['image_urls']]

        # дата записи

        props_container = response.css(".detail__props .props")

        record = None
        release = None
        props_lines = []

        for block in props_container.css(".props__prop"):
            label = clean_text(block.css(".props__label::text").get())
            value_text = clean_text(" ".join(block.css(".props__value ::text").getall()))

            if not label:
                continue  # пустая метка — это, например, музыкальные ссылки, разберём отдельно

            if label.strip(':') == "Запись":
                record = value_text
            elif label.strip(':') == "Выпуск":
                release = value_text
            else:
                # собираем в текст: "Метка: значение"
                props_lines.append(f"{label} {value_text}")

        # сохраняем
        item['date_of_record'] = record
        item['release'] = release
        item['props_text'] = "\n".join(props_lines) if props_lines else None

        # ссылки
        item['links'] = extract_music_links(props_container, response.url)

        # # описание (credits/cast)
        # p_nodes = response.css(".description__content > p")
        # credits_lines = get_paragraph_lines(p_nodes[0]) if len(p_nodes) >= 1 else []
        # cast_lines = get_paragraph_lines(p_nodes[1]) if len(p_nodes) >= 2 else []
        # item['credits'] = parse_credits(credits_lines)
        # item['cast'] = parse_cast(cast_lines)

        # описание — весь текст из description__content
        description_text = " ".join(
            clean_text(t) for t in response.css(".description__content ::text").getall() if clean_text(t)
        )
        item['description'] = description_text

        # # (необязательно) каталог. номер как имя папки
        # for block in props_container.css(".props__prop"):
        #     label = clean_text(block.css(".props__label::text").get())
        #     if label and "Номер в каталоге" in label:
        #         cat = clean_text(" ".join(block.css(".props__value ::text").getall()))
        #         item['folder_hint'] = cat
        #         break

        yield item

    # def parse_detail(self, response):
    #     item = MelodyparserItem()
    #     item['title'] = response.css("h1::text").get()
    #     item['image_urls'] = response.css("div.gallery__slide img::attr(src)").getall()
    #
    #     # если пути относительные — превратим в абсолютные
    #     item['image_urls'] = [response.urljoin(url) for url in item['image_urls']]
    #
    #
    #
    #     # ---- record (дата записи) из props ----
    #     record = None
    #     props_container = response.css(".detail__props .props")
    #     for block in props_container.css(".props__prop"):
    #         label = clean_text(block.css(".props__label::text").get())
    #         if label and label.strip(':') == "Запись":
    #             record_text = clean_text(" ".join(block.css(".props__value ::text").getall()))
    #             # можно дополнительно нормализовать до года:
    #             # m = re.search(r'\b(19|20)\d{2}\b', record_text or '')
    #             # record = m.group(0) if m else record_text
    #             record = record_text
    #             break
    #
    #     item['date_of_record'] = record
    #
    #     # ---- музыкальные ссылки из props (блок с <a>) ----
    #     links = extract_music_links(props_container, response.url)
    #
    #     item['links'] = links
    #
    #     # ---- credits & cast из двух параграфов ----
    #     p_nodes = response.css(".description__content > p")
    #     credits_lines = get_paragraph_lines(p_nodes[0]) if len(p_nodes) >= 1 else []
    #     cast_lines = get_paragraph_lines(p_nodes[1]) if len(p_nodes) >= 2 else []
    #
    #     credits = parse_credits(credits_lines)
    #     item['credits'] = credits
    #
    #     cast = parse_cast(cast_lines)
    #     item['cast'] = cast
    #     yield item
    #
    #
    #
    #     # yield item
    #     # Парсим детальную информацию
    #     # yield {
    #     #     "title": response.css("h1::text").get(),
    #     #     # "text": response.css("div.content p::text").getall(),
    #     #     "images": response.css("picture.gallery__picture img::attr(src)").getall(),
    #     #     # "links": response.css("a::attr(href)").getall()
    #     # }
