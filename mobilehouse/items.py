# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MobileHouseItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Brand = scrapy.Field()
    Price = scrapy.Field()
    Video = scrapy.Field()
    USB = scrapy.Field()
    WiFi = scrapy.Field()
    Speed = scrapy.Field()
    Ram = scrapy.Field()
    Bluetooth = scrapy.Field()

