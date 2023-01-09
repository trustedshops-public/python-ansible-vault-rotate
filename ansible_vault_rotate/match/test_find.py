import unittest

from .find import find_vault_strings


class MatchFindTest(unittest.TestCase):

    def load_results(self, file_name: str):
        return [item for item in find_vault_strings(f"match/__testdata__/{file_name}.yml")]

    def test_find_single(self):
        results = self.load_results("single_vaulted")
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertIsNone(result['label'])
        self.assertEqual(result['indent'], '  ')

    def test_find_labeled(self):
        results = self.load_results("label_vaulted")
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result['label'], "dev")
        self.assertEqual(result['indent'], '  ')

    def test_find_nested(self):
        results = self.load_results("nested_vaulted")
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result['label'], "dev")
        self.assertEqual(result['indent'], '    ')
