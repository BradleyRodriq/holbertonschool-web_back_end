#!/usr/bin/env python3
""" Cache class """
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """
    incr
    """
    @wraps(method)
    def increment(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return increment


class Cache:
    """
    connection to redis
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data as db
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        gets the value for key
        """
        result = self._redis.get(key)

        if fn is not None:
            result = fn(result)

        return result

    def get_str(self, key):
        """
        returns string value
        """
        return self.get(key, lambda x: x.decode())

    def get_int(self, key):
        """
        returns int value
        """
        return self.get(key, lambda x: int(x.decode()))
