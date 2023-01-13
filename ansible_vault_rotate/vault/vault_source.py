from abc import ABC, abstractmethod


class VaultSource(ABC):
    """
    Implement this method to enable a different source for vault secrets
    """

    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, value: str) -> None:
        pass


class FileVaultSource(VaultSource):
    """
    Implementation of VaultSource to load secret from file
    """

    def __open_file(self, mode: str):
        return open(self.source.replace("file://", ""), mode)

    def read(self) -> str:
        with self.__open_file("r") as f:
            return f.read().rstrip()

    def write(self, value: str) -> None:
        with self.__open_file("w") as f:
            f.write(value)


class TextVaultSource(VaultSource):
    """
    Implementation of VaultSource to load secret from given text
    """

    def read(self) -> str:
        return self.source

    def write(self, value: str) -> None:
        # noop
        pass


def build_vault_source(raw: str) -> VaultSource:
    """
    Construct correct VaultSource based on input provided
    :param raw: Raw text
    """
    if raw.startswith("file://"):
        return FileVaultSource(raw)
    else:
        return TextVaultSource(raw)
