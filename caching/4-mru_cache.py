#!/usr/bin/env python3
""" MRU cache """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU cache class """
    def __init__(self):
        """ Constructor """
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
            mru_key = self.keys.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")
        self.cache_data[key] = item
        self.keys.append(key)
