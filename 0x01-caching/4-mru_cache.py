#!/usr/bin/env python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a caching system using MRU (Most Recently Used) algorithm.
    It manages the cache by discarding the most recently used item when the cache limit is exceeded.
    """

    def __init__(self):
        """ Initialize the MRU cache.
        
        This method calls the parent class initializer to set up the cache_data dictionary.
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item to the cache using MRU method.
        
        This method assigns the value item to the key key in the cache_data dictionary.
        If either key or item is None, the method does not do anything.
        If the number of items exceeds MAX_ITEMS, the most recently used item is discarded.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the value and mark it as the most recently used
                self.cache_data[key] = item
                self.order.remove(key)
                self.order.append(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Discard the most recently used item
                    mru_key = self.order.pop()  # Last item in the list is the MRU
                    self.cache_data.pop(mru_key)
                    print("DISCARD: {}".format(mru_key))
                self.cache_data[key] = item
                self.order.append(key)

    def get(self, key):
        """ Get an item by key from the cache.
        
        This method retrieves the value associated with the key in the cache_data dictionary.
        If the key is None or does not exist, it returns None. Also updates the order for MRU.
        """
        if key is None:
            return None
        if key in self.cache_data:
            # Update the order to mark this key as most recently used
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
