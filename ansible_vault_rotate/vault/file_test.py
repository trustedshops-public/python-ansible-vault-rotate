import os
import unittest
from tempfile import NamedTemporaryFile
from ansible_vault_rotate.vault import load_with_vault
from .file import rekey_file


class VaultFileTest(unittest.TestCase):
    def test_single_secret(self):
        with NamedTemporaryFile("r", delete=True) as f:
            rekey_file(os.path.dirname(os.path.abspath(__file__)) + "/__testdata__/single-secret.yml", "test", "test123", f.name)
            lines = f.readlines()
            self.assertEqual(len(lines), 8)

            doc = load_with_vault(f.name, "default", "test123")
            self.assertEqual(doc['regular_key'], "goes here")
            self.assertEqual(doc['test'], 'test')

    def test_multiple_secret(self):
        with NamedTemporaryFile("r", delete=True) as f:
            rekey_file(os.path.dirname(os.path.abspath(__file__)) + "/__testdata__/multiple-secret.yml", "test", "test123", f.name)
            lines = f.readlines()
            self.assertEqual(len(lines), 17)

            doc = load_with_vault(f.name, "default", "test123")
            self.assertEqual(doc['regular_key'], "goes here")
            self.assertEqual(doc['my_key']['a'], 'test')
            self.assertEqual(doc['my_key']['b'], 'abc')
