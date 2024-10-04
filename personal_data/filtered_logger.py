#!/usr/bin/env python3
""" filtered logger """
from typing import List
import re
import logging
from os import environ
import mysql.connector

PII_FIELDS = "email", "name", "ssn", "password", "phone"


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


def get_logger() -> logging.Logger:
    """_summary_

    Returns:
        logging.Logger: _description_
    """
    result: logging.Logger = logging.getLogger("user_data")
    result.setLevel(logging.INFO)
    result.propagate = False
    handler = logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    result.addHandler(handler)
    return result


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    _summary_
    """
    return mysql.connector.connect(
        user=environ.get("PERSONAL_DATA_DB_USERNAME"),
        password=environ.get("PERSONAL_DATA_DB_PASSWORD"),
        host=environ.get("PERSONAL_DATA_DB_HOST"),
        database=environ.get("PERSONAL_DATA_DB_NAME")
    )
