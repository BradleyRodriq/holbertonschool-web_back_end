#!/usr/bin/env python3
""" Cache class """
from uuid import uuid4
from typing import Union
import redis


class Cache:
    """
    connection to redis
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data as db
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
