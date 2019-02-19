#! /usr/bin/rnv python3
# -*- coding:utf-8 -*-

import scrapy

from search.settings import DEFAULT_REQUEST_HEADERS


class GoogleSpider(scrapy.Spider):
    name = 'google'

    def __init__(self, kw, pn=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kw = str(kw)
        self.pn = int(pn)
        DEFAULT_REQUEST_HEADERS['Host'] = 'www.google.com'
        DEFAULT_REQUEST_HEADERS['Referer'] = 'https://www.google.com/'
        self.header = DEFAULT_REQUEST_HEADERS

    def start_requests(self):
        urls = [
            'https://www.google.com/search?q={}&start={}0'.format(
                self.kw, self.pn
                )
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.header,
                callback=self.parse
                )

    def parse(self, response):
        results = response.xpath('//div[@class="rc"]').getall()
        print(results)
        # for result in results:
        #    print(result)
        related = response.xpath('//div[@class="card-section"]')
        print(related)
