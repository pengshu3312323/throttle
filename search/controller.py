
import time
import logging
import logging.handlers
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from search.server import SearchServer
from search import settings

logger = logging.getLogger('error')
logger.setLevel(logging.ERROR)

logging.basicConfig(datefmt=settings.LOG_DATE_FORMAT)

handler = logging.handlers.RotatingFileHandler(
    settings.LOG_FILE_NAME,
    maxBytes=1024 * 1024,
    backupCount=5
    )
handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))

logger.addHandler(handler)


class SearchServerController:
    def __new__(cls, *args, **kwargs):
        '''singleton'''
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, worker_num=10):
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
