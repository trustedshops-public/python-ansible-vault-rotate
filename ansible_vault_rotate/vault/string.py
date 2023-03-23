import typing
from tempfile import NamedTemporaryFile
from ansible.parsing.vault import VaultEditor, VaultLib, VaultSecret
from ansible_vault_rotate.match import FindVaultStringResult
from os import remove
from .util import create_vault_lib, create_vault_secret


def vault_string(vault_string_search_result: FindVaultStringResult, old_passphrase: str, new_passphrase: str) -> str:
    """
    Rekey a given vault string search result by decrypting the passphrase and rekeying with new passphrase

    Secret data is never written to disk in the process

    :param vault_string_search_result: Details about the vaulted string
    :param old_passphrase: Old passphrase to decrypt
    :param new_passphrase: New passphrase to encrypt the secret in after decryption
    :return: Indented and with new passphrase vaulted string
    """
    indent = vault_string_search_result['indent']
    vaulted_string = vault_string_search_result['vaultedString']
    label = vault_string_search_result['label']

    # write vaulted text to file
    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(vaulted_string.replace(indent, ''))
        temp_file = f

    if temp_file is None:
        raise IOError("Could not create temporary file for rekey")

    # rekey file
    editor = VaultEditor(create_vault_lib(label, old_passphrase))
    editor.rekey_file(temp_file.name, create_vault_secret(new_passphrase), label)

    # read content and add indentation again
    with open(f.name, "r") as f:
        new_vault = indent + indent.join(f.readlines()).rstrip()
        content = vaulted_string.replace(vaulted_string, new_vault)

    # delete temp file and return ready to use string
    remove(f.name)
    return content
