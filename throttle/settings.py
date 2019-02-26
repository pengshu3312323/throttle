# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

if DEBUG:
    RABBITMQ = {
        'host': 'localhost',
        'port': 5672,
        'username': 'pencil',
        'password': 'hummel165'
    }
else:
    RABBITMQ = {
        'host': '172.17.0.1',
        'port': 5672,
        'username': 'pencil',
        'password': 'hummel165'
    }

# 生产者等待响应超时时间
RABBITMQ_RESPONSE_TIMEOUT = 5

# 日志配置
LOG_FILE_NAME = BASE_DIR + '/log/error.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# redis
if DEBUG:
    REDIS = {
      'host': '127.0.0.1',
      'port': 6879,
      'password': 'hummel165',
    }
else:
    REDIS = {
        'host': '172.17.0.1',
        'port': 6879,
        'password': 'hummel165',
    }
