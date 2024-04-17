import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from unsplash_scraper.items import UnsplashScraperItem

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ["https://unsplash.com/napi/photos?page=1&per_page=12"]


    def parse(self, response:HtmlResponse):
        data = response.json()
        for item in data:
            loader = ItemLoader(item=UnsplashScraperItem())
            loader.add_value('author', item['user']['name'])
            loader.add_value('description', item['alt_description'])
            loader.add_value('url', item['urls']['raw'])
            loader.add_value('image_path','')
            yield loader.load_item()


        # Получаю номер текущей страницы из параметров URL
        current_page = int(response.url.split('page=')[1].split('&')[0])
        next_page = current_page + 1

        # Создаю URL для следующей страницы
        next_page_url = f"https://unsplash.com/napi/photos?page={next_page}&per_page=12"

        # Проверка, есть ли еще страницы для обработки
        # if len(data) > 0:
        if next_page < 10:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                dont_filter=True
            )
