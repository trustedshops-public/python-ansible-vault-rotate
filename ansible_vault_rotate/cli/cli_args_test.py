import unittest
import sys
from .cli_args import has_cli_args, parse_args

class CliArgsTest(unittest.TestCase):
    def test_has_cli_args(self):
        sys.argv = []
        self.assertFalse(has_cli_args())
