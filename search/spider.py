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
        # results = selector.xpath('//div[@class="rc"]')
        item_list = []
        titles = selector.xpath('//h3[@class="LC20lb"]')
        sources = selector.xpath('//cite[@class="iUh30"]')
        dess = selector.xpath('//span[@class="st"]')
        for t, s, d in zip(titles, sources, dess):
            item = dict(
                search_type='google',
                keyword=keyword,
                page_num=pn
                )
            item['title'] = t
            item['source'] = s
            item['des'] = d

            item_list.append(item)
        return item_list
