#! /usr/bin/env python3

import time
import uuid
import json

import pika

from search.settings import RABBITMQ, RABBITMQ_RESPONSE_TIMEOUT
from search.base import RabbitMQBase


class SearchClient(RabbitMQBase):
    '''搜索 生产者（客户端）'''
    def __init__(self):
        self._connect()
        # 声明 exchange 和 queue
        self.channel.exchange_declare(
            exchange='search',
            exchange_type='direct'
        )
        # 这个queue是响应队列
        self.queue = self.channel.queue_declare(exclusive=True)
        # 一个消费者消费完了才发送下一个消息
        self.channel.basic_qos(prefetch_count=1)
        # 处理 响应 队列
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.queue.method.queue
            )

    def send(self, keyword, pn=0, search_type=0):
        if not keyword:
            # 必须要有关键词
            print('keyword is empty')
            return 0

        msg = self.build_msg(keyword, pn)
        print(type(msg), msg)
        self.response = None  # 是否收到响应
        self.corr_id = str(uuid.uuid4())
        if search_type == 0:
            # 谷歌搜索
            self.channel.basic_publish(
                exchange='search',
                routing_key='google',
                properties=pika.BasicProperties(
                    reply_to=self.queue.method.queue,
                    correlation_id=self.corr_id
                ),
                body=msg
            )
        else:
            print('不支持的类型')
            pass
        print('Sent msg :{}'.format(msg))
        start_time = time.time()
        wait_time = 0
        while self.response is None:
            # 等待到收到响应为止
            self.connection.process_data_events()
            wait_time = time.time() - start_time
            if wait_time > RABBITMQ_RESPONSE_TIMEOUT:
                print('Response timeout')
                return 0
        print('Received response : {}'.format(self.response))
        return 1

    def build_msg(self, keyword, pn):
        # 拼装搜索关键字和页码
        msg = {
            'keyword': str(keyword),
            'pn': pn,
        }
        return json.dumps(msg)

    def on_response(self, ch, method, properties, body):
        # 响应处理
        if self.corr_id == properties.correlation_id:
            # 响应匹配
            self.response = str(body)

    def close(self):
        self.connection.close()
        print('Connection closed')
