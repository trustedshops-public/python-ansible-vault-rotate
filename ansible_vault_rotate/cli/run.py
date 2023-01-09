from ansible_vault_rotate import __VERSION__
from argparse import ArgumentParser


def run():
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=f'%(prog)s {__VERSION__}')
    args = parser.parse_args()
