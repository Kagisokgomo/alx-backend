#!/usr/bin/env python3
""" FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache defines a caching system using FIFO (First In, First Out) algorithm.
    It manages the cache by discarding the oldest item when the cache limit is exceeded.
    """

    def __init__(self):
        """ Initialize the FIFO cache.
        
        This method calls the parent class initializer to set up the cache_data dictionary.
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item to the cache using FIFO method.
        
        This method assigns the value item to the key key in the cache_data dictionary.
        If either key or item is None, the method does not do anything.
        If the number of items exceeds MAX_ITEMS, the oldest item is discarded.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Get the first inserted key
                first_key = next(iter(self.cache_data))
                # Discard the oldest item
                discarded_item = self.cache_data.pop(first_key)
                print("DISCARD: {}".format(first_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key from the cache.
        
        This method retrieves the value associated with the key in the cache_data dictionary.
        If the key is None or does not exist, it returns None.
        """
        if key is None:
            return None
        return self.cache_data.get(key)
