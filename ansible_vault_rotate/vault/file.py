import typing

from ansible.errors import AnsibleError

from .string import vault_string
from ansible_vault_rotate.match import find_vault_strings


def rekey_file(source: str, old_passphrase: str, new_passphrase: str, target: typing.Union[str, None] = None) -> int:
    """
    Rekey all ansible vault secrets in the given file
    :param source: Path to source file
    :param old_passphrase: Old passphrase to decrypt secrets
    :param new_passphrase: New passphrase to encrypt secrets with
    :param target: Target path, if not specified overwrites source path
    :return: Amount of replaced secrets
    """
    replacements = []
    for match in find_vault_strings(source):
        try:
            replacement = vault_string(match, old_passphrase, new_passphrase)
            replacements.append((match, replacement))
        except AnsibleError as e:
            # Ignore decryption errors
            if "Decryption failed" not in str(e):
                raise e
    if len(replacements) == 0:
        raise AnsibleError("Decryption failed (no vault secrets were found that could decrypt)")

    with open(source, "r") as file_to_rekey:
        file_content = file_to_rekey.read()

    if target is None:
        target = source

    with open(target, "w") as file_to_rekey:
        for match, replacement in replacements:
            file_content = file_content.replace(match['vaultedString'], replacement)

        file_to_rekey.write(file_content)

    return len(replacements)
