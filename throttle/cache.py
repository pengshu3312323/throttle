import random
import pickle
from functools import wraps

import redis

from throttle.settings import REDIS
from throttle.log import logger


class Cache:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, connections_num=10):
        self.pool = redis.ConnectionPool(
            host=REDIS['host'],
            port=REDIS['port'],
            password=REDIS['password'],
            max_connections=connections_num
        )
        self.r = redis.StrictRedis(connection_pool=self.pool)

    def set(self, key, value, time=600):
        '''
        Set value to cache
        key -> str
        return: None or 1
        '''
        if not isinstance(key, str):
            logger.error('Cache key must be string', exc_info=True)
            return None
        try:
            time = int(time)
        except Exception:
            logger.error('Time must be numbers', exc_info=True)
            return None

        time = int(time * (10 + random.randint(0, 3)) / 10)
        return self.r.set(key, pickle.dumps(value), time)

    def get(self, key):
        '''
        Get value from cache
        key -> str
        return: None or value
        '''
        if not isinstance(key, str):
            logger.error('Cache key must be string', exc_info=True)
            return None

        try:
            value_b = self.r.get(key)
            value = pickle.loads(value_b) if value_b is not None else value_b
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
        else:
            return value

    def delete(self, key):
        '''
        Delete value from cache
        '''
        if not isinstance(key, str):
            logger.error('Cache key must be string', exc_info=True)
            return None

        return self.r.delete(key)


cache = Cache()


def cache_control(time=60):
    '''
    Decorator for class method
    First, get value from cache, if no value in the cache,
    run the class method and set the result to the cache
    '''
    def decorator(func):
        cache_key_prefix = 'search_' + func.__name__ + '_'
        @wraps(func)
        def wraper(self, *args, **kwargs):
            cache_key = cache_key_prefix + \
                '_'.join(str(arg) for arg in args) + \
                '_'.join(str(k) + str(v) for k, v in kwargs.items())
            cache_value = cache.get(cache_key)
            if cache_value:
                return cache_value
            new_value = func(self, *args, **kwargs)
            cache.set(cache_key, new_value, time)
            return new_value
        return wraper
    return decorator
