#!/usr/bin/env python3
"""concurrent coroutines"""
import asyncio
from typing import List

randwait = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """wait n"""
    routines = [randwait(max_delay) for i in range(n)]
    return [await x for x in asyncio.as_completed(routines)]
