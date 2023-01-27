import unittest
from .tui import validate_present, when_type, remap_vault_source

class TuiTest(unittest.TestCase):
    def test_validate_present(self):
        self.assertFalse(validate_present(""))
        self.assertTrue(validate_present("test"))

    def test_when_type(self):
        callback = when_type("old","file")
        self.assertTrue(callback({
            "old_vault.type": "file"
        }))

        self.assertFalse(callback({
            "old_vault.type": "plain text"
        }))

    def test_remap_vault_source(self):
        args = {
            "old_vault.type": "file",
            "old_vault.value": "vault.txt"
        }
        remap_vault_source(args, "old")
        print(args)
        self.assertIn("old_vault_secret_source", args)
        self.assertEqual(args['old_vault_secret_source'],  "file://vault.txt")
