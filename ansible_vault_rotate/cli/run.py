import sys
import logging

from .logging import FormattingConsoleLogHandler
from .cli_args import parse_args
from .config import CliConfig
from .rotator import AnsibleVaultRotator


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
