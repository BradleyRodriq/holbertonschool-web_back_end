#!/usr/bin/env python3
"""Async generator"""
import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None, None]:
    """async generator"""
    for i in range(0, 10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
