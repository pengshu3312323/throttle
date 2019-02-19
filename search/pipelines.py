# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json


class GooglePipeline:
    def __init__(self):
        now = int(time.time())
        file_name = 'google_{}.json'.format(now)
        self.file = open(file_name, "at")

    def process_item(self, item, spider):
        # Stored as json
        lines = json.dumps(dict(item)) + "\n"
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()
