#!/usr/bin/env python3
"""Measure runtime"""
import asyncio
import time

wait = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """measure runtime"""
    start_time = time.perf_counter()
    asyncio.run(wait(n, max_delay))
    end_time = time.perf_counter()
    return (end_time - start_time) / n
