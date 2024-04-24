#!/usr/bin/env python3
"""Measure runtime"""
import asyncio
import time

async_comp = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure runtime"""
    start = time.perf_counter()
    await asyncio.gather(*[async_comp() for i in range(4)])
    """await asyncio.gather(
        async_comp(),
        async_comp(),
        async_comp(),
        async_comp()
    )"""
    end = time.perf_counter()
    return end - start
