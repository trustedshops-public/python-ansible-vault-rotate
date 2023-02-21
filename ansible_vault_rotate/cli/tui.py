from InquirerPy import prompt, get_style
from InquirerPy.validator import PathValidator
from os import getcwd
from unittest.mock import patch


VAULT_TYPE_FILE = "file"
VAULT_TYPE_PLAIN_TEXT = "plain text"
VAULT_TYPES = [
    VAULT_TYPE_PLAIN_TEXT,
    VAULT_TYPE_FILE,
]


def validate_present(value: str) -> bool:
    """
    Validate a given parameter is present
    :param value: Value to check
    """
    return len(value) > 0


def when_type(specifier: str, type: str) -> callable:
    """
    Run the given input when the vault is of the given type
    :param specifier: Specifier of vault (old, new)
    :param type: Type of the vault source secret
    """
    def inner(result):
        return result[f"{specifier}_vault.type"] == type

    return inner


def remap_vault_source(args: dict[str], specifier: str) -> None:
    """
    Remap the vault source from interactive input
    :param args: Arguments collected
    :param specifier: Specifier of vault (old, new)
    """
    prefix = ""
    vault_type = args[f"{specifier}_vault.type"]
    normalized_vault_type = vault_type.replace(" ","_")

    if vault_type == "file":
        prefix = "file://"

    args[f"{specifier}_vault_secret_source"] = f"{prefix}{args[f'{specifier}_vault.value.{normalized_vault_type}']}"


validate_directory = PathValidator(is_dir=False, message="Input is not a file")
questions = [
    {
        "type": "list",
        "name": "old_vault.type",
        "message": "Old Vault Secret Source > Type",
        "choices": VAULT_TYPES,
    },
    {
        "type": "input",
        "name": "old_vault.value.plain_text",
        "message": "Old Vault Secret Source > Value (Text)",
        "when": when_type("old", VAULT_TYPE_PLAIN_TEXT),
        "validate": validate_present,
        "invalid_message": "Old vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "old_vault.value.file",
        "message": "Old Vault Secret Source > Value (File)",
        "when": when_type("old", VAULT_TYPE_FILE),
        "validate": validate_directory,
    },
    {
        "type": "list",
        "name": "new_vault.type",
        "message": "New Vault Secret Source > Type",
        "choices": VAULT_TYPES,
    },
    {
        "type": "input",
        "name": "new_vault.value.plain_text",
        "message": "Old Vault Secret Source > Value (Text)",
        "when": when_type("new", VAULT_TYPE_PLAIN_TEXT),
        "validate": validate_present,
        "invalid_message": "New vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "new_vault.value.file",
        "message": "New Vault Secret Source > Value (File)",
        "when": when_type("new", "file"),
        "validate": validate_directory,
    },
    {
        "type": "filepath",
        "name": "pwd",
        "message": "Working directory for execution, this also changes the relative path for file urls",
        "default": getcwd(),
    },
    {
        "type": "confirm",
        "name": "ignore_errors",
        "message": "Should we ignore when an error occurs processing individual files?",
    },
    {
        "type": "confirm",
        "name": "update_source_secret",
        "message": "Should the source secret be updated?",
        "when": when_type("old", VAULT_TYPE_FILE),
    },
]


def prompt_tui() -> dict[str]:
    args = prompt(questions)
    remap_vault_source(args, "old")
    remap_vault_source(args, "new")
    return args
