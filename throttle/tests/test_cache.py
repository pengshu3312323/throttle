#! /usr/bin/env python3

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__name__)))
sys.path.append(BASE_DIR)

import pytest

from throttle.cache import cache_control


class FakeServer:
    @cache_control(5)
    def get(self, keyword, pn=0):
        print('No cache')
        # return keyword + str(pn) + '\n'


class TestCache:
    def setup(self):
        print('test start')
        self.server = FakeServer()

    def test_cache(self):
        keyword_1 = 'python'
        pn_1 = 0
        keyword_2 = 'go'
        pn_2 = 1

        res_1 = self.server.get(keyword_1, pn_1)
        res_2 = self.server.get(keyword_1, pn_1)
        res_3 = self.server.get(keyword_2, pn_2)
        time.sleep(6)
        res_4 = self.server.get(keyword_1, pn_1)
        print(res_1, res_2, res_3, res_4)

        assert (res_2 == res_1) and (res_3 != res_1)
