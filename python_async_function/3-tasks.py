#!/usr/bin/env python3
"""the regular function syntax task 3"""
import asyncio

randwait = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """task wait random"""
    return asyncio.create_task(randwait(max_delay))
