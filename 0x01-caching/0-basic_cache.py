#!/usr/bin/env python3
""" BasicCache module
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache defines a caching system without limit.
    It allows adding and retrieving items from the cache.
    """

    def put(self, key, item):
        """ Add an item to the cache.
        
        This method assigns the value item to the key key in the cache_data dictionary.
        If either key or item is None, the method does not do anything.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key from the cache.
        
        This method retrieves the value associated with the key in the cache_data dictionary.
        If the key is None or does not exist, it returns None.
        """
        if key is None:
            return None
        return self.cache_data.get(key)
