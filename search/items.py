# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchItem(scrapy.Item):
    search_type = scrapy.Field()  # 搜索方式 百度还是谷歌
    keyword = scrapy.Field()  # 关键字
    page_num = scrapy.Field()  # 搜索页码
    title = scrapy.Field()  # 标题
    des = scrapy.Field()   # 描述
    source = scrapy.Field()  # 来源
