import logging
import unittest
from .logging import FormattingConsoleLogHandler
from logging import LogRecord


class LoggingTest(unittest.TestCase):
    def test_format(self):
        handler = FormattingConsoleLogHandler()
        record = LogRecord("test", logging.INFO, "test.py", 20, "my message", {}, None)
        formatted = handler.format(record)
        self.assertIsNotNone(formatted)
