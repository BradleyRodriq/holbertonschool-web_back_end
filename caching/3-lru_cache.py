#!/usr/bin/env python3
""" 3-lru_cache.py """
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU cache class """
    def __init__(self):
        super().__init__()
        self.keys = []

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        self.keys.remove(key)
        self.keys.append(key)
        return self.cache_data[key]

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.keys.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            oldest_key = self.keys.pop(0)
            del self.cache_data[oldest_key]
            print(f"DISCARD: {oldest_key}")
        self.cache_data[key] = item
        self.keys.append(key)
