import os
import unittest
from .vault_source import TextVaultSource, FileVaultSource, build_vault_source


class VaultSourceTest(unittest.TestCase):
    def fixture_name(self, file_name: str) -> str:
        return os.path.dirname(os.path.abspath(__file__)) + f"/__testdata__/{file_name}"

    def test_text_source(self):
        text = TextVaultSource("text")
        self.assertEqual(text.read(), "text")

    def test_file_source(self):
        file = FileVaultSource(f"file://{self.fixture_name('vault-password')}")
        self.assertEqual(file.read(), "test")

    def test_build_text(self):
        source = build_vault_source("test")
        self.assertIsInstance(source, TextVaultSource)

    def test_build_file(self):
        source = build_vault_source("file://test.txt")
        self.assertIsInstance(source, FileVaultSource)
