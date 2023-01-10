import os
import unittest
from .detect import has_vault_secrets


class DetectTest(unittest.TestCase):
    def fixture_name(self, file_name: str) -> str:
        return os.path.dirname(os.path.abspath(__file__)) + f"/__testdata__/{file_name}"

    def test_vault_file(self):
        self.assertTrue(has_vault_secrets(self.fixture_name("vaulted-file.txt")))

    def test_inline_secrets(self):
        self.assertTrue(has_vault_secrets(self.fixture_name("multiple-secret.yml")))

    def test_no_match(self):
        self.assertFalse(has_vault_secrets(self.fixture_name("vault-password")))
