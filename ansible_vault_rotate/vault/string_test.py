import unittest
from .string import vault_string
from ansible_vault_rotate.match import FindVaultStringResult


class VaultStringTest(unittest.TestCase):
    def verify_indent(self, result, indent):
        lines = result.split("\n")
        for line in lines:
            if line == "":
                continue
            self.assertTrue(line.startswith(indent), "line '%s' is not indented" % line)
        self.assertEqual(len(lines), 7)

    def test_rekey_unlabeled(self):
        search_result = FindVaultStringResult(
            vaultedString="""  $ANSIBLE_VAULT;1.1;AES256
      34636530313034373261383234633232653732316262383339653836323862306263613432623935
      6536646366356261386539343166333065356432663264650a313566316439356364663032346639
      64396563353261333239643163303933343265666433666632333535336565313331613863383936
      6662356434666238370a346334643536653462333164643464383233623830393766333561316538
      3333""",
            indent='  ',
            label=None)

        result = vault_string(search_result, "test", "test123")
        self.assertIsNotNone(result)
        self.verify_indent(result, '  ')

    def test_rekey_labeled(self):
        search_result = FindVaultStringResult(
            vaultedString="""  $ANSIBLE_VAULT;1.1;AES256;dev
          34636530313034373261383234633232653732316262383339653836323862306263613432623935
          6536646366356261386539343166333065356432663264650a313566316439356364663032346639
          64396563353261333239643163303933343265666433666632333535336565313331613863383936
          6662356434666238370a346334643536653462333164643464383233623830393766333561316538
          3333""",
            indent='  ',
            label='dev')

        result = vault_string(search_result, "test", "test123")
        self.assertIn('dev', result)
        self.assertIsNotNone(result)
        self.verify_indent(result, '  ')
