#! /usr/bin/env python3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__name__))
sys.path.append(BASE_DIR)

from concurrent.futures import ThreadPoolExecutor, as_completed

from throttle.server import SearchServer
from throttle.log import logger


class SearchServerController:
    '''
    Control the consumer(server)
    '''
    def __new__(cls, *args, **kwargs):
        '''singleton'''
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, worker_num=6):
        self._server_started = False
        self.worker_num = int(worker_num)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.worker_num)

    def _start_a_worker(self):
        # 启动一个 Search 消费者（服务器）
        server = SearchServer()
        server.google_consume()

    def start(self):
        if self._server_started:
            print('No more')
            return 0
        self.tasks = [
            self.thread_pool.submit(self._start_a_worker) for _ in range(self.worker_num)
            ]
        self._server_started = True
        print('Workers start finished')

        for future in as_completed(self.tasks):
            # 捕获异常并重启
            try:
                future.result()
            except Exception as e:
                # 重新开始一个线程
                logger.error(e, exc_info=True)
                self.thread_pool.submit(self._start_a_worker)
                print('Worker restarted')


if __name__ == '__main__':
    c = SearchServerController()
    c.start()
