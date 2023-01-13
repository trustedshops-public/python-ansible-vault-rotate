import os
import unittest
from .glob import iterate_patterns


class GlobTest(unittest.TestCase):
    def __build_glob(self, relative_pattern: str) -> str:
        return os.path.dirname(os.path.abspath(__file__)) + f"/__testdata__/glob/{relative_pattern}"

    def test_top_level_glob(self):
        files = [file for file in iterate_patterns([self.__build_glob("*")])]
        self.assertEqual(len(files), 2)

    def test_nested_glob(self):
        files = [file for file in iterate_patterns([self.__build_glob("**/*")])]
        self.assertEqual(len(files), 3)
