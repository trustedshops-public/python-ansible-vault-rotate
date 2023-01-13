import logging
from .config import CliConfig
from .glob import iterate_patterns
from ..vault import has_vault_secrets, rekey_file


class AnsibleVaultRotator:
    def __init__(self, config: CliConfig):
        self.config = config
        self.error_count = 0
        self.rekeyed_files_count = 0
        self.rekey_secrets_count = 0

    def iterate_files(self) -> "AnsibleVaultRotator":
        for file_path in iterate_patterns(self.config.file_glob_patterns):
            logging.debug("Found file %s", file_path)
            if not has_vault_secrets(file_path):
                logging.debug("File has no secrets, skipping")
                continue

            logging.info("Processing file %s", file_path)
            try:
                self.__track_secrets_count(
                    rekey_file(file_path,
                               self.config.source_vault_passphrase,
                               self.config.target_vault_passphrase)
                )
            except Exception as e:
                self.__handle_error(file_path, e)

        return self

    def __handle_error(self, file_path: str, e: Exception) -> None:
        self.error_count += 1
        if self.config.ignore_errors:
            logging.warning("Failed to rekey file %s: %s", file_path, e)
        else:
            logging.error("Failed to rekey file %s: %s", file_path, e)
            raise e

    def __track_secrets_count(self, secrets_count: int) -> None:
        self.rekey_secrets_count += secrets_count
        self.rekeyed_files_count += 1
