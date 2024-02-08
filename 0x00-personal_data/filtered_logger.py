#!/usr/bin/env python3
"""Function called filter_datum"""
import re
from typing import List
import logging
import mysql.connector
import csv
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes and accepts list of fields strings"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connect to MySQL environment """
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

    return db_connect


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """implementation of the filter_datum function"""
    for result in fields:
        message = re.sub(f'{result}=(.*?){separator}',
                         f'{result}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Create a logger named "user_data" with INFO level"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter())
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


def main() -> None:
    """Database connection using get_db"""
    db_connection = get_db()
    cursor = db_connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")
    result = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, result))
        logger.info(str_row.strip())

    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    main()
