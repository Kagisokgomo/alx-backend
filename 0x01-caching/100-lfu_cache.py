#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines a caching system using LFU (Least Frequently Used) algorithm.
    It manages the cache by discarding the least frequently used item when the cache limit is exceeded.
    If there are multiple candidates, it uses LRU (Least Recently Used) to determine which to discard.
    """

    def __init__(self):
        """ Initialize the LFU cache.
        
        This method calls the parent class initializer to set up the cache_data dictionary.
        """
        super().__init__()
        self.frequency = {}
        self.order = []
    
    def put(self, key, item):
        """ Add an item to the cache using LFU method.
        
        This method assigns the value item to the key key in the cache_data dictionary.
        If either key or item is None, the method does not do anything.
        If the number of items exceeds MAX_ITEMS, the least frequently used item is discarded,
        and if there's a tie, the least recently used among them is discarded.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the value and frequency
                self.cache_data[key] = item
                self.frequency[key] += 1
                # Update the order to mark this key as most recently used
                self.order.remove(key)
                self.order.append(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Find the least frequently used key
                    lfu_keys = [k for k, v in self.frequency.items() if v == min(self.frequency.values())]
                    if len(lfu_keys) > 1:
                        # Apply LRU to break the tie
                        lfu_key = None
                        for k in self.order:
                            if k in lfu_keys:
                                lfu_key = k
                                break
                    else:
                        lfu_key = lfu_keys[0]
                    
                    # Discard the LFU key
                    self.cache_data.pop(lfu_key)
                    self.frequency.pop(lfu_key)
                    self.order.remove(lfu_key)
                    print("DISCARD: {}".format(lfu_key))

                # Add new item
                self.cache_data[key] = item
                self.frequency[key] = 1
                self.order.append(key)

    def get(self, key):
        """ Get an item by key from the cache.
        
        This method retrieves the value associated with the key in the cache_data dictionary.
        If the key is None or does not exist, it returns None. Also updates frequency and order.
        """
        if key is None:
            return None
        if key in self.cache_data:
            # Update frequency and order
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
