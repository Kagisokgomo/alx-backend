#!/usr/bin/env python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines a caching system using LIFO (Last In, First Out) algorithm.
    It manages the cache by discarding the most recently added item when the cache limit is exceeded.
    """

    def __init__(self):
        """ Initialize the LIFO cache.
        
        This method calls the parent class initializer to set up the cache_data dictionary.
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item to the cache using LIFO method.
        
        This method assigns the value item to the key key in the cache_data dictionary.
        If either key or item is None, the method does not do anything.
        If the number of items exceeds MAX_ITEMS, the most recently added item is discarded.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Get the last inserted key
                last_key = list(self.cache_data.keys())[-1]
                # Discard the most recently added item
                discarded_item = self.cache_data.pop(last_key)
                print("DISCARD: {}".format(last_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key from the cache.
        
        This method retrieves the value associated with the key in the cache_data dictionary.
        If the key is None or does not exist, it returns None.
        """
        if key is None:
            return None
        return self.cache_data.get(key)
