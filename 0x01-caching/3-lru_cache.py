#!/usr/bin/env python3
""" LRUCache module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache defines a caching system using the LRU (Least Recently Used) algorithm.
    This caching system manages memory by discarding the least recently accessed items
    when the cache limit is exceeded.
    """

    def __init__(self):
        """ Initialize the LRU cache.
        
        This method invokes the parent class initializer to establish the cache_data dictionary.
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item to the cache using the LRU method.
        
        This method associates the value item with the key key in the cache_data dictionary.
        If either key or item is None, this method refrains from performing any action.
        In scenarios where the count of items exceeds MAX_ITEMS, the least recently used
        item is discarded, and the key of the discarded item is printed.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the item if it already exists
                self.cache_data[key] = item
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Discard the least recently used item
                    lru_key = next(iter(self.cache_data))
                    print("DISCARD: {}".format(lru_key))
                    self.cache_data.pop(lru_key)
                self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item by key from the cache.
        
        This method returns the value linked to the specified key in the cache_data dictionary.
        If the key is None or does not exist, it returns None.
        Additionally, upon access, the item is updated as the most recently used.
        """
        if key is None:
            return None
        if key in self.cache_data:
            # Move the accessed item to the end to mark it as recently used
            item = self.cache_data[key]
            del self.cache_data[key]
            self.cache_data[key] = item
            return item
        return None
