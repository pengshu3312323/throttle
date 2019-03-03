#! /usr/bin/rnv python3
# -*- coding:utf-8 -*-

import json

import requests
from lxml import etree

from throttle.settings import DEFAULT_REQUEST_HEADERS


class GoogleSpider:
    def __init__(self):
        DEFAULT_REQUEST_HEADERS['Host'] = 'www.google.com'
        DEFAULT_REQUEST_HEADERS['Referer'] = 'https://www.google.com/'
        self.header = DEFAULT_REQUEST_HEADERS

    def fake_results(self):
        item_list = []
        for i in range(10):
            item = dict()
            item['search_type'] = 'g'
            item['keyword'] = 'keyword'
            item['page_num'] = 0

            item['title'] = '这是标题_{}'.format(i)
            item['source'] = 'source_{}'.format(i)
            item['des'] = '<div><span>这是详情<em>{}<em></span></div>'.format(i)

            item_list.append(item)
        return item_list

    def start_requests(self, keyword, pn=0):
        data = {
            'success': False,
            'data': '',
        }

        if not keyword:
            # 当关键字为空时，直接失败
            return data

        url = 'https://www.google.com/search?q={}&start={}0'.format(
            keyword, pn
            )
        res = requests.get(
            url=url,
            headers=self.header
            )

        selector = etree.HTML(str(res.content, 'utf-8'))
        results = selector.xpath('//div[@class="rc"]')

        if not results:
            return data

        item_list = []
        # item_list = self.fake_results()

        for result in results:
            res_str = etree.tostring(result)
            res_selector = etree.HTML(res_str)
            title = res_selector.xpath('//h3[@class="LC20lb"]/text()')[0]
            source = res_selector.xpath('//div[@class="r"]/a/@href')[0]
            des = res_selector.xpath('//span[@class="st"]')[0]

            item = dict()
            item['search_type'] = 'g'
            item['keyword'] = keyword
            item['page_num'] = pn

            # Element, ElementUnicodeResult 对象 转utf-8 字符串
            title_str = str(title)
            source_str = str(source)
            des_str = etree.tostring(des, encoding='utf-8').decode(encoding='utf-8')

            item['title'] = title_str if title_str else ''
            item['source'] = source_str if source_str else ''
            item['des'] = des_str if des_str else ''

            item_list.append(item)

        data['success'] = True
        data['data'] = item_list

        return data
