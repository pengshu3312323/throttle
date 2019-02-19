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

        selector = etree.HTML(res)
        results = selector.xpath('//div[@class="rc"]')
        item_list = []
        for res in results:
            title = res.xpath('//h3[@class="LC20lb"]').get()
            source = res.xpath('//cite[@class="iUh30"]').get()
            des = res.xpath('//span[@class="st"]').get()
            item = dict(
                search_type='google',
                keyword=keyword,
                page_num=pn
                )
            item['title'] = title
            item['source'] = source
            item['des'] = des

            item_list.append(item)
        return item_list
