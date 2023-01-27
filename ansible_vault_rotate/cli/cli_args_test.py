import unittest
from unittest.mock import patch
from .cli_args import has_cli_args, parse_args


class CliArgsTest(unittest.TestCase):
    def test_has_cli_args(self):
        with patch("sys.argv", ["bin", "-h"]):
            self.assertTrue(has_cli_args())
