import os
import unittest
from tempfile import NamedTemporaryFile

from ansible.parsing.vault import VaultEditor
from ansible.parsing.dataloader import DataLoader

from ansible_vault_rotate.vault import load_with_vault
from ansible_vault_rotate.vault.util import create_vault_secret
from .file import rekey_file
from .util import create_vault_lib


class VaultFileTest(unittest.TestCase):
    def fixture_name(self, file_name: str) -> str:
        return os.path.dirname(os.path.abspath(__file__)) + f"/__testdata__/{file_name}"

    def assertLineCount(self, f: NamedTemporaryFile, count: int):
        lines = f.readlines()
        self.assertEqual(len(lines), count)
        f.seek(0)

    def test_single_secret(self):
        with NamedTemporaryFile("r", delete=False) as f:
            rekey_file(self.fixture_name("single-secret.yml"), "test", "test123", f.name)

            self.assertLineCount(f, 8)

            os.chdir("/tmp") # work around for ansible path resolve issues
            doc = load_with_vault(f.name, "default", "test123")
            self.assertEqual(doc['regular_key'], "goes here")
            self.assertEqual(doc['test'], 'test')

    def test_single_secret_eof(self):
        with NamedTemporaryFile("r", delete=False) as f:
            rekey_file(self.fixture_name("single-secret-eof.yml"), "test", "test123", f.name)

            self.assertLineCount(f, 7)

            os.chdir("/tmp") # work around for ansible path resolve issues
            doc = load_with_vault(f.name, "default", "test123")
            self.assertEqual(doc['test'], 'test')

    def test_multiple_secret(self):
        with NamedTemporaryFile("r", delete=False) as f:
            rekey_file(self.fixture_name("multiple-secret.yml"), "test", "test123", f.name)

            self.assertLineCount(f, 17)

            os.chdir("/tmp") # work around for ansible path resolve issues
            doc = load_with_vault(f.name, "default", "test123")
            self.assertEqual(doc['regular_key'], "goes here")
            self.assertEqual(doc['my_key']['a'], 'test')
            self.assertEqual(doc['my_key']['b'], 'abc')

    def test_vault_file(self):
        with NamedTemporaryFile("r", delete=True) as f:
            rekey_file(self.fixture_name("vaulted-file.txt"), "test", "test123", f.name)

            self.assertLineCount(f, 6)

            editor = VaultEditor(create_vault_lib("default", "test123"))
            content = editor.plaintext(f.name).decode("utf8")
            self.assertEqual(content, "i am\na multiline\nstring\n")

    def test_multiple_vault(self):
        with NamedTemporaryFile("r", delete=True) as f:
            rekey_file(self.fixture_name("multiple-vault.yml"), "testprod", "testprod123", f.name)

            self.assertLineCount(f, 17)
            os.chdir("/tmp") # work around for ansible path resolve issues

            loader = DataLoader()
            loader.set_vault_secrets(([
                ("dev", create_vault_secret("test")),
                ("prod", create_vault_secret("testprod123")),
            ]))
            doc = loader.load_from_file(f.name)
            self.assertEqual(doc['regular_key'], "goes here")
            self.assertEqual(doc['my_key']['a'], 'test')
            self.assertEqual(doc['my_key']['b'], 'abc')
