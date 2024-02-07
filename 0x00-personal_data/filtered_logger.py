#!/usr/bin/env python3
"""Function called filter_datum"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """implementation of the filter_datum function"""
    for result in fields:
        message = re.sub(f'{result}=(.*?){separator}',
                         f'{result}={redaction}{separator}', message)
    return message
