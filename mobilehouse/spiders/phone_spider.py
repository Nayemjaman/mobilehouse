import scrapy


class PhoneSpiderSpider(scrapy.Spider):
    name = 'phone_spider'
    allowed_domains = ['gsmarena.com.bd']
    start_urls = ['http://gsmarena.com.bd/']

    def parse(self, response):
        pass
