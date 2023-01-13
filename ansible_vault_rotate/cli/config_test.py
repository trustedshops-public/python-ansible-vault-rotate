import unittest
from .config import CliConfig


class ConfigTest(unittest.TestCase):
    def test_glob_pattern_default(self):
        config = CliConfig({})
        self.assertEqual(config.file_glob_patterns, ["**/*.yml", "**/*.yaml"])

    def test_glob_pattern_custom(self):
        config = CliConfig({
            'file_glob_pattern': ['**/*.yml']
        })
        self.assertEqual(len(config.file_glob_patterns), 1)
        self.assertEqual(config.file_glob_patterns[0], "**/*.yml")

    def test_parse(self):
        config = CliConfig({
            'old_vault_secret_source': "old-secret",
            'new_vault_secret_source': "new-secret",
        })
        config.parse_vaults()

        self.assertIsNotNone(config.source_vault)
        self.assertIsNotNone(config.target_vault)

        self.assertEqual(config.source_vault_passphrase, "old-secret")
        self.assertEqual(config.target_vault_passphrase, "new-secret")
