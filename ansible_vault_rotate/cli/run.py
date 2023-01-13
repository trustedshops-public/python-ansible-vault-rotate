import sys
import logging
from ansible_vault_rotate.vault import has_vault_secrets, rekey_file

from .logging import FormattingConsoleLogHandler
from .cli_args import parse_args
from .config import CliConfig
from .glob import iterate_patterns


def run() -> None:
    """
    Entrypoint for CLI
    """
    logging.basicConfig(level=logging.INFO, handlers=[FormattingConsoleLogHandler()])

    args = parse_args()
    logging.debug("Arguments provided: %s", args)

    config = CliConfig(args.__dict__)
    config.switch_to_pwd()

    try:
        config.parse_vaults()
    except Exception as e:
        logging.error("Failed to load vault sources", e)
        sys.exit(2)

    error_count = 0
    rekeyed_files_count = 0
    rekey_secrets_count = 0

    for file in iterate_patterns(config.file_glob_patterns):
        logging.debug("Found file %s", file)
        if not has_vault_secrets(file):
            continue

        logging.info("Processing file %s", file)
        try:
            rekey_secrets_count += rekey_file(file, config.source_vault_passphrase, config.target_vault_passphrase)
            rekeyed_files_count += 1
        except Exception as e:
            error_count += 1
            if config.ignore_errors:
                logging.warning("Failed to rekey file %s: %s", file, e)
            else:
                logging.error("Failed to rekey file %s: %s", file, e)
                sys.exit(1)

    logging.info(
        f"Finished rotation | Errors: {error_count}, Rekeyed secrets: {rekey_secrets_count}, Rekeyed files: {rekeyed_files_count}")

    if config.update_source_secret:
        logging.info("Try to update source secret")
        config.source_vault.write(config.target_vault_passphrase)
