#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict

class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Get a page of the dataset with hypermedia pagination.

        Args:
            index (int): The starting index of the page (default is None).
            page_size (int): The number of items per page (default is 10).

        Returns:
            Dict: A dictionary containing pagination details.
        
        Raises:
            AssertionError: If index is out of range.
        """
        assert index is not None and index >= 0, "Index must be a non-negative integer"
        
        indexed_data = self.indexed_dataset()
        total_items = len(indexed_data)
        
        if index >= total_items:
            raise AssertionError("Index is out of range")

        data = []
        for i in range(index, index + page_size):
            if i in indexed_data:
                data.append(indexed_data[i])
            else:
                page_size -= 1  # Adjust page size if an item is missing

        next_index = index + page_size
        return {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index if next_index < total_items else None
        }
