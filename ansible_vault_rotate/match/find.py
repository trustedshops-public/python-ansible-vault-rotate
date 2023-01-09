import re
import typing

ANSIBLE_VAULT_REGEX = re.compile(r'(^(\s*)\$ANSIBLE_VAULT;(\S*)\n(\s*\w+\n)*)', re.MULTILINE)


class FindVaultStringResult(typing.TypedDict):
    vaultedString: str
    label: typing.Union[str, None]
    indent: str


def find_vault_strings(file_path: str) -> typing.Generator[FindVaultStringResult, None, None]:
    with open(file_path, "r") as f:
        content = "".join(f.readlines())
        for match in ANSIBLE_VAULT_REGEX.findall(content):
            meta = match[2].split(";")

            yield FindVaultStringResult(
                vaultedString=match[0].strip(),
                label=meta[2] if len(meta) == 3 else None,
                indent=match[1]
            )
