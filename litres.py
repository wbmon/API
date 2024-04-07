import scrapy
from scrapy.http import HtmlResponse
from litparser.items import LitparserItem


class LitresSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/genres/978/?page=1"]

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//div[@class="pagination-next"]//@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@class="cover genres-cover"]//@href').getall()
        for link in links:
            yield response.follow(link, callback=self.liter_parse)

    def liter_parse(self, response: HtmlResponse):
        name = response.xpath('//div[@class="prodtitle"]/h1/text()').getall()
        salary = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        autor = response.xpath('//div[@class="authors"]/a/text()').getall()
        about = response.xpath('//div[@id="product-about"]//text()').getall()
        url = response.url
        yield LitparserItem(name=name, salary=salary, autor=autor, about=about, url=url)
