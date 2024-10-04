#!/usr/bin/env python3
""" filtered logger """
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """_summary_
    """
    result = message
    for field in fields:
        construct = f"(?<={field}=)(.*?)(?={separator})"
        result = re.sub(construct, redaction, result)
    return result


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)

        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """ _summary_"""
        message: str = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )
