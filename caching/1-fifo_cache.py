#!/user/bin/env python3
""" 1-fifo_cache.py """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO cache class """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.keys_queue = []
        
    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.keys_queue.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            oldest_key = self.keys_queue.pop(0)
            del self.cache_data[oldest_key]
            print(f"DISCARD: {oldest_key}")
        self.cache_data[key] = item
        self.keys_queue.append(key)
            
    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)