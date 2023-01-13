import os
import unittest
from .rotator import AnsibleVaultRotator
from .config import CliConfig
import tempfile
import shutil


class AnsibleVaultRotatorTest(unittest.TestCase):
    def data_folder(self, path):
        return os.path.dirname(os.path.abspath(__file__)) + f"/__testdata__/{path}"

    def test_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = CliConfig({
                'old_vault_secret_source': 'test',
                'new_vault_secret_source': 'test',
                'pwd': str(tmpdir)
            })
            config.switch_to_pwd()
            config.parse_vaults()
            rotator = AnsibleVaultRotator(config)
            rotator.iterate_files()
            self.assertEqual(rotator.rekeyed_files_count, 0)
            self.assertEqual(rotator.rekey_secrets_count, 0)
            self.assertEqual(rotator.error_count, 0)

    def test_valid_vault(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = shutil.copytree(self.data_folder("vaulted"), str(tmpdir) + "/test")
            config = CliConfig({
                'old_vault_secret_source': 'test',
                'new_vault_secret_source': 'test',
                'pwd': str(path)
            })
            config.switch_to_pwd()
            config.parse_vaults()
            rotator = AnsibleVaultRotator(config)
            rotator.iterate_files()
            self.assertEqual(rotator.rekeyed_files_count, 1)
            self.assertEqual(rotator.rekey_secrets_count, 1)
            self.assertEqual(rotator.error_count, 0)

    def test_invalid_vault(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = shutil.copytree(self.data_folder("vaulted"), str(tmpdir) + "/test")
            config = CliConfig({
                'old_vault_secret_source': 'test123',
                'new_vault_secret_source': 'test',
                'pwd': str(path),
                'ignore_errors': True,
            })
            config.switch_to_pwd()
            config.parse_vaults()
            rotator = AnsibleVaultRotator(config)
            rotator.iterate_files()
            self.assertEqual(rotator.rekeyed_files_count, 0)
            self.assertEqual(rotator.rekey_secrets_count, 0)
            self.assertEqual(rotator.error_count, 1)
