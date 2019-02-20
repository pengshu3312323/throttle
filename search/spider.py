#! /usr/bin/rnv python3
# -*- coding:utf-8 -*-

import scrapy
import requests
from lxml import etree

from search.settings import DEFAULT_REQUEST_HEADERS


class GoogleSpider:
    def __init__(self):
        DEFAULT_REQUEST_HEADERS['Host'] = 'www.google.com'
        DEFAULT_REQUEST_HEADERS['Referer'] = 'https://www.google.com/'
        self.header = DEFAULT_REQUEST_HEADERS

    def start_requests(self, keyword, pn=0):
        url = 'https://www.google.com/search?q={}&start={}0'.format(
            keyword, pn
            )
        res = requests.get(
            url=url,
            headers=self.header
            )

        selector = etree.HTML(res.text)
        results = selector.xpath('//div[@class="rc"]')
        item_list = []

        for res in results:
            res_str = etree.tostring(res, encoding='utf-8')
            res_selector = etree.HTML(res_str)
            title = res_selector.xpath('//h3[@class="LC20lb"]/text()')
            source = res_selector.xpath('//div[@class="r"]/a/@href')
            des = res_selector.xpath('//span[@class="st"]')

            item = dict()
            item['search_type'] = 'g'
            item['keyword'] = keyword
            item['page_num'] = pn
            item['title'] = title
            item['source'] = source
            item['des'] = etree.tostring(des).decode('utf-8')

            item_list.append(item)
        return item_list
