import sys
import logging

from .logging import FormattingConsoleLogHandler
from .cli_args import parse_args, has_cli_args
from .config import CliConfig
from .rotator import AnsibleVaultRotator
from .tui import prompt_tui


def run() -> None:
    """
    Entrypoint for CLI
    """
    logging.basicConfig(level=logging.INFO, handlers=[FormattingConsoleLogHandler()])
    if has_cli_args():
        args = parse_args()
        args = args.__dict__
        is_interactive = False
    else:
        args = prompt_tui()
        is_interactive = True
        print()

    logging.debug("Arguments provided: %s", args)

    config = CliConfig(args)
    config.switch_to_pwd()

    try:
        config.parse_vaults()
    except Exception as e:
        logging.error("Failed to load vault sources: %s", e)
        sys.exit(2)

    rotator = AnsibleVaultRotator(config)
    try:
        rotator.iterate_files()
    except Exception as e:
        sys.exit(1)

    logging.info(f"Finished rotation | "
                 f"Errors: {rotator.error_count}, "
                 f"Rekeyed secrets: {rotator.rekey_secrets_count}, "
                 f"Rekeyed files: {rotator.rekeyed_files_count}")

    if config.update_source_secret:
        logging.info("Try to update source secret")
        config.source_vault.write(config.target_vault_passphrase)

    if is_interactive:
        print("")
        print("\033[1mThe options you chose resulted in the following CLI call. You can use that for automation as well.\033[0m")
        print(f"  \033[3m{config.to_cli_call_string()}\033[0m")
