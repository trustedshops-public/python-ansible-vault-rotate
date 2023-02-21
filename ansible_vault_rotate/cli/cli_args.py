from argparse import ArgumentParser, Namespace
from os import getcwd
import sys

from ansible_vault_rotate import __VERSION__

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
parser.add_argument("--update-source-secret",
                    action="store_true",
                    help="Should the source secret be updated (not supported for text source)",
                    default=False)


def has_cli_args():
    return len(sys.argv) != 1


def parse_args() -> Namespace:
    return parser.parse_args()
