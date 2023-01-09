from tempfile import NamedTemporaryFile
from ansible.parsing.vault import VaultEditor, VaultLib, VaultSecret
from ansible_vault_rotate.match import FindVaultStringResult


def vault_string(vault_string_search_result: FindVaultStringResult, old_passphrase: str, new_passphrase: str):
    indent = vault_string_search_result['indent']
    vaulted_string = vault_string_search_result['vaultedString']
    label = vault_string_search_result['label']

    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(vaulted_string.replace(indent, ''))
        tempFile = f

    if tempFile is None:
        raise IOError("Could not create temporary file for rekey")

    editor = VaultEditor(VaultLib([
        (label if label is not None else "default", VaultSecret(old_passphrase.encode()))
    ]))
    editor.rekey_file(tempFile.name, VaultSecret(new_passphrase.encode()), label)
    with open(f.name, "r") as f:
        new_vault = indent + indent.join(f.readlines()).rstrip()
        content = vaulted_string.replace(vaulted_string, new_vault)

    return content
