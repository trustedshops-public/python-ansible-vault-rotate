from InquirerPy import prompt
from InquirerPy.validator import PathValidator
from os import getcwd

VAULT_TYPES = [
    "plain text",
    "file",
]

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
        "when": lambda result: result["old_vault.type"] == "plain text",
        "validate": lambda result: len(result) > 0,
        "invalid_message": "Old vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "old_vault.value",
        "message": "Old Vault Secret Source > Value (File)",
        "when": lambda result: result["old_vault.type"] == "file",
        "validate": PathValidator(is_dir=False, message="Input is not a file"),
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
        "when": lambda result: result["new_vault.type"] == "plain text",
        "validate": lambda result: len(result) > 0,
        "invalid_message": "New vault passphrase needs to be set",
    },
    {
        "type": "filepath",
        "name": "new_vault.value",
        "message": "New Vault Secret Source > Value (File)",
        "when": lambda result: result["new_vault.type"] == "file",
        "validate": PathValidator(is_dir=False, message="Input is not a file"),
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
        "message": "Should we abort when an error occurs processing individual files?",
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

    args[f"{specifier}_vault_secret_source"] = f"{prefix}.{args[f'{specifier}_vault.value']}"

    del args[f"{specifier}_vault.type"]
    del args[f'{specifier}_vault.value']


def prompt_tui():
    args = prompt(questions)
    remap_vault_source(args, "old")
    remap_vault_source(args, "new")
    return args
