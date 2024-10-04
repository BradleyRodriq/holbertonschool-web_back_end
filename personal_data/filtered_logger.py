#!/usr/bin/env python3
""" filtered logger """
from typing import List
import re


def filter_datum( fields: List[str], redaction: str, message: str, separator: str) -> str:
    """_summary_
    """
    result = message
    for field in fields:
        construct = f"(?<={field}=)(.*?)(?={separator})"
        result = re.sub(construct, redaction, result)
    return result
