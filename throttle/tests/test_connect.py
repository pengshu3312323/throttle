#! /usr/bin/env python3
import os
import sys
import json

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__name__)))
sys.path.append(BASE_DIR)

from throttle.base import RabbitMQBase


class Server(RabbitMQBase):
    def __init__(self):
        self._connect()
        self.queue = self.channel.queue_declare(queue='test')

    def start_consume(self):
        self.channel.basic_consume(
            self.callback,
            queue='test',
            no_ack=True
        )
        print('Server established')

    def callback(self, method, properties, body):
        msg = body.decode(encoding='utf-8')
        msg = json.loads(msg)


class Client(RabbitMQBase):
    def __init__(self):
        self._connect()
        self.queue = self.channel.queue_declare(queue='test')

    def send(self, msg):
        msg = json.dumps(msg)
        self.channel.basic_publish(
            exchange='',
            routing_key='test',
            body=msg
        )
        print('Msg published')


class TestConnect:
    def setup(self):
        self.msg1 = 'this is string'
        self.msg2 = 5
        self.msg3 = [1, 2, 3]
        self.msg4 = {'a': 5}
        self.server = Server()
        self.client = Client()
        self.server.start_consume()

    def test_1(self):
        self.client.send(self.msg1)
        assert True

    def test_2(self):
        self.client.send(self.msg2)
        assert True

    def test_3(self):
        self.client.send(self.msg3)
        assert True

    def test_4(self):
        self.client.send(self.msg4)
        assert True
