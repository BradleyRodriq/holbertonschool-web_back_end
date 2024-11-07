#!/usr/bin/env python3
""" Cache class """
from uuid import uuid4
from typing import Union, Optional, Callable, List
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


def call_history(method: Callable) -> Callable:
    """
    keeps track of input and output
    """
    @wraps(method)
    def log(self, *args, **kwargs):
        inputs = args
        output = method(self, *args, **kwargs)

        self._redis.rpush(
            f"{method.__qualname__}:inputs", str(inputs)
        )

        self._redis.rpush(
            f"{method.__qualname__}:outputs", str(output)
        )

        return output
    return log


def replay(method: Callable) -> None:
    """
    methods history
    """
    redis_tunnel = redis.Redis()

    inputs: List[bytes] = \
        redis_tunnel.lrange(f"{method.__qualname__}:inputs", 0, -1)
    outputs: List[bytes] = \
        redis_tunnel.lrange(f"{method.__qualname__}:outputs", 0, -1)
    call_count: int = int(redis_tunnel.get(f"{method.__qualname__}"))

    print(f"{method.__qualname__} was called {call_count} times:")

    for input, output in zip(inputs, outputs):
        input = input.decode()
        output = output.decode()

        print(
            f"{method.__qualname__}(*{input}) -> {output}"
        )


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
