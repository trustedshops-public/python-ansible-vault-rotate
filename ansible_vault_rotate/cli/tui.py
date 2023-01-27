from InquirerPy import prompt, get_style
from InquirerPy.validator import PathValidator
from os import getcwd

VAULT_TYPES = [
    "plain text",
    "file",
]


def validate_present(result):
    return len(result) > 0


def when_type(specifier, type):
    def inner(result):
        return result[f"{specifier}_vault.type"] == type

    return inner


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
        "name": "old_vault.value",
        "message": "Old Vault Secret Source > Value (Text)",
        "when": when_type("old", "plain text"),
        "validate": validate_present,
        "invalid_message": "Old vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "old_vault.value",
        "message": "Old Vault Secret Source > Value (File)",
        "when": when_type("old", "file"),
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
        "name": "new_vault.value",
        "message": "Old Vault Secret Source > Value (Text)",
        "when": when_type("new", "plain text"),
        "validate": validate_present,
        "invalid_message": "New vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "new_vault.value",
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
        "when": lambda result: result["old_vault.type"] == "file",
    },
]


def remap_vault_source(args, specifier):
    prefix = ""
    if args[f"{specifier}_vault.type"] == "file":
        prefix = "file://"

    args[f"{specifier}_vault_secret_source"] = f"{prefix}{args[f'{specifier}_vault.value']}"

    del args[f"{specifier}_vault.type"]
    del args[f'{specifier}_vault.value']


def prompt_tui():
    args = prompt(questions)
    remap_vault_source(args, "old")
    remap_vault_source(args, "new")
    return args
