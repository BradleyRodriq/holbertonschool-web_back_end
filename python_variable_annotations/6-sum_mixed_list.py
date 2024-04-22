#!/usr/bin/env python3
"""mixed list"""
from typing import List, Union


def sum_mixed_list(lst: List[Union[int, float]]) -> float:
    """return float: a sum of all nums inside a list"""
    return sum(lst)
