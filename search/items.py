# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    title = scrapy.Field()   # 标题
    des = scrapy.Field()     # 描述
    source = scrapy.Field()  # 来源


class GoogleItem(scrapy.Item):
    keyword = scrapy.Field()   # 关键字
    page_num = scrapy.Field()  # 搜索页码
    result = scrapy.Field()    # 单页所有的结果
    related = scrapy.Field()   # 相关搜索
