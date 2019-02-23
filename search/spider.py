#! /usr/bin/rnv python3
# -*- coding:utf-8 -*-

import json

import requests
from lxml import etree

from search.settings import DEFAULT_REQUEST_HEADERS


class GoogleSpider:
    def __init__(self):
        DEFAULT_REQUEST_HEADERS['Host'] = 'www.google.com'
        DEFAULT_REQUEST_HEADERS['Referer'] = 'https://www.google.com/'
        self.header = DEFAULT_REQUEST_HEADERS

    def start_requests(self, keyword, pn=0):
        res = {
            'success': False,
            'data': '',
        }

        if not keyword:
            # 当关键字为空时，直接失败
            return json.dumps(res)

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

        if not results:
            return json.dumps(res)

        for res in results:
            res_str = etree.tostring(res)
            res_selector = etree.HTML(res_str)
            title = res_selector.xpath('//h3[@class="LC20lb"]/text()')[0]
            source = res_selector.xpath('//div[@class="r"]/a/@href')[0]
            des = res_selector.xpath('//span[@class="st"]')[0]

            item = dict()
            item['search_type'] = 'g'
            item['keyword'] = keyword
            item['page_num'] = pn
            item['title'] = title if title else ''
            item['source'] = source if source else ''
            item['des'] = str(etree.tostring(des)) if des else ''

            item_list.append(item)

        res['success'] = True
        res['data'] = item_list

        return json.dumps(res)
