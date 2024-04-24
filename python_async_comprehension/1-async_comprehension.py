#!/usr/bin/env python3
"""Async comprehension"""
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> list():
    """async comprehension"""
    return [i async for i in async_generator()]
