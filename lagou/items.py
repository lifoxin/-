# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job = scrapy.Field()
    money = scrapy.Field()
    company = scrapy.Field()
    required = scrapy.Field()
    place = scrapy.Field()

class ImageItem(scrapy.Item):
    images = scrapy.Field()                       #下载图片存放的地址
    images_urls = scrapy.Field()   				  #下载图片必须有的