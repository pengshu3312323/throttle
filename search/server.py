#! /usr/bin/env python3

import time
import random
import json

import pika

from search.settings import RABBITMQ
from search.base import RabbitMQBase
from search.spider import GoogleSpider


class SearchServer(RabbitMQBase):
    def __init__(self):
        self._connect()
        # 声明 exchange 和 queue
        self.channel.exchange_declare(
            exchange='search',
            exchange_type='direct'
        )
        self.queue = self.channel.queue_declare()

    def google_consume(self):
        # 绑定到键为 google 的队列
        self.channel.queue_bind(
            exchange='search',
            queue=self.queue.method.queue,
            routing_key='google'
        )
        self.channel.basic_consume(
            self.google_handler,
            queue=self.queue.method.queue
        )
        print('Waiting for google search msg....')
        self.channel.start_consuming()

    def google_handler(self, ch, method, properties, body):
        # 处理收到的body
        print(type(body), body)
        body = json.loads(body)
        keyword = body.get('keyword', '')
        pn = body.get('pn', 0)

        res = self.spider_start(keyword, pn)

        # 发送结果到响应队列 exchange和接收的不同
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
                ),
            body=str(res)
            )
        # 消息确认
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('Web search finished')

    def work_simulation(self):
        # 模拟爬取
        time_used = random.randint(1, 5)
        time.sleep(time_used)
        return time_used

    def spider_start(self, keyword, pn):

        # 返回 爬取结果，json格式
        s = GoogleSpider()
        return s.start_requests(keyword, pn)
