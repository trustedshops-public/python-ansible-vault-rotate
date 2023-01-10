import sys
from os import getcwd, chdir
import logging
from glob import glob
from argparse import ArgumentParser

from ansible_vault_rotate import __VERSION__
from ansible_vault_rotate.vault import build_vault_source, has_vault_secrets, rekey_file

from .logging import FormattingConsoleLogHandler


def run() -> None:
    """
    Entrypoint for CLI
    """
    logging.basicConfig(level=logging.DEBUG, handlers=[FormattingConsoleLogHandler()])

    parser = ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {__VERSION__}',
                        help="Print current version and exit")
    parser.add_argument("--old-vault-secret-source",
                        type=str,
                        help="Source for the old secret. Valid are only plain text or file urls starting with file:// and pointing to a file relative to the current directory or absolute paths",
                        required=True)
    parser.add_argument("--new-vault-secret-source",
                        type=str,
                        help="Source for the new secret. Valid are only plain text or file urls starting with file:// and pointing to a file relative to the current directory or absolute paths",
                        required=True)
    parser.add_argument("--file-glob-pattern",
                        type=str,
                        action="append",
                        help="Glob pattern to apply the rekey for.",
                        default=[])
    parser.add_argument("--ignore-errors",
                        action="store_true",
                        help="Do not abort on processing individual files",
                        default=False)
    parser.add_argument("--pwd",
                        type=str,
                        help="Change working directory for execution, this also changes the relative path for file urls",
                        default=getcwd())
    args = parser.parse_args()
    logging.debug("CLI Args: %s", args)

    chdir(args.pwd)
    source_vault_passphrase = build_vault_source(args.old_vault_secret_source).read()
    target_vault_passphrase = build_vault_source(args.new_vault_secret_source).read()

    file_glob_pattern = args.file_glob_pattern
    ignore_errors = args.ignore_errors

    if len(file_glob_pattern) == 0:
        file_glob_pattern = ["**/*.yml", "**/*.yaml"]

    error_count = 0
    rekeyed_files_count = 0
    rekey_secrets_count = 0
    for pattern in file_glob_pattern:
        for file in glob(pattern, recursive=True):
            logging.debug("Found file %s", file)
            if has_vault_secrets(file):
                logging.info("Processing file %s", file)
                try:
                    rekey_secrets_count += rekey_file(file, source_vault_passphrase, target_vault_passphrase)
                    rekeyed_files_count += 1
                except Exception as e:
                    error_count += 1
                    if ignore_errors:
                        logging.warning("Failed to rekey file %s: %s", file, e)
                    else:
                        logging.error("Failed to rekey file %s: %s", file, e)
                        sys.exit(1)

    logging.info(f"Finished rotation | Errors: {error_count}, Rekeyed secrets: {rekey_secrets_count}, Rekeyed files: {rekeyed_files_count}")
