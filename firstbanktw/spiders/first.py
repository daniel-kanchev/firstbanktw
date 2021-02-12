import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from firstbanktw.items import Article


class FirstSpider(scrapy.Spider):
    name = 'first'
    start_urls = ['https://www.firstbank.com.tw/sites/fbweb/NewsReleases']

    def parse(self, response):
        links = response.xpath('//div[@class="col-lg-4 col-md-6 col-sm-6 news-item"]//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="content-title"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="date mb5"]//text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="content-body"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[2:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
