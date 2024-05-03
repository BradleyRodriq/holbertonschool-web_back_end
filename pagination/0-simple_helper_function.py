#!/usr/bin/env python3
""" simple helper function """
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ index range """
    idx = page * page_size - page_size
    index = idx + page_size
    return (idx, index)
