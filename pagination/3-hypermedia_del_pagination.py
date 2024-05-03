#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(index=None, page_size=10) -> Dict:
        """ get hyper index """
        dataset_size = 100
        deleted_rows = {3, 6, 7}

        assert index is None or (isinstance(index, int) and index >= 0)
        assert page_size > 0

        current_index = index if index is not None else 0
        if current_index >= dataset_size:
            return {}

        next_index = min(current_index + page_size, dataset_size)

        deleted_rows_before_next_index = len([r for r in deleted_rows if r < next_index])
        next_index += deleted_rows_before_next_index

        data = list(range(current_index, min(next_index, dataset_size)))

        return {
            "index": current_index,
            "next_index": next_index,
            "page_size": page_size,
            "data": data
        }
