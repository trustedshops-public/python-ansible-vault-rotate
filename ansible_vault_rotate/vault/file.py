import typing

from .string import vault_string
from ansible_vault_rotate.match import find_vault_strings


def rekey_file(source: str, old_passphrase: str, new_passphrase: str, target: typing.Union[str, None] = None):
    replacements = []
    for match in find_vault_strings(source):
        replacement = vault_string(match, old_passphrase, new_passphrase)
        replacements.append((match, replacement))

    with open(source, "r") as file_to_rekey:
        file_content = file_to_rekey.read()

    if target is None:
        target = source

    with open(target, "w") as file_to_rekey:
        for match, replacement in replacements:
            file_content = file_content.replace(match['vaultedString'], replacement)

        file_to_rekey.write(file_content)
