import typing

from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.parsing.dataloader import DataLoader


def create_vault_secret(passphrase: str) -> VaultSecret:
    return VaultSecret(passphrase.encode())


def create_vault_lib(label: typing.Union[str, None], passphrase: str) -> VaultLib:
    return VaultLib([
        (label if label is not None else "default", create_vault_secret(passphrase))
    ])


def load_with_vault(path: str, vault_label: str, passphrase: str) -> dict:
    loader = DataLoader()
    loader.set_vault_secrets(([(vault_label, create_vault_secret(passphrase))]))
    return loader.load_from_file(path)
