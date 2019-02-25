#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__name__)))
sys.path.append(BASE_DIR)

from search.client import SearchClient


class TestClients:
    '''模拟 client'''
    def set_one_client(self, keyword, pn=0):
        client = SearchClient()
        res = client.send(keyword, pn=pn)
        print(res)
        client.close()
        return res

    def setup(self):
        self.pool = ThreadPoolExecutor(max_workers=5)
        print('Test begin')

    def test_a(self):
        msgs = [('python', 0), ('java', 1), ('c++', 0), ('go', 1)]
        tasks = [
            self.pool.submit(self.set_one_client, m) for m in msgs
            ]

        response = list()
        for future in as_completed(tasks):
            res = future.result()
            print(res)
            response.append(res)

        assert all(response)
