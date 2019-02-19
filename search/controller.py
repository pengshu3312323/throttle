
import time
from concurrent.futures import ThreadPoolExecutor

from scrapy.crawler import CrawlerProcess

from search.spiders.baidu_spider import BaiduSpider
from search.spiders.google_spider import GoogleSpider


class Controller:
    def __init__(self):
        self._thread_pool = ThreadPoolExecutor(max_workers=10)

    def crawl(self, type, keyword, pn=0):
        time.sleep(2)  # 假装在爬取
        return 1

    def execute(self):
        task = self._thread_pool.submit(self.crawl('baidu', 'test'))
        return task
