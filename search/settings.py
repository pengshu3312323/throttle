# -*- coding: utf-8 -*-

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
   'Connection': 'keep-alive',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}


RABBITMQ = {
   'host': 'localhost',
   'port': 5672,
   'username': 'pencil',
   'password': 'hummel165'
}


RABBITMQ_RESPONSE_TIMEOUT = 5
