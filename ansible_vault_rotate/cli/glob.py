import typing
from glob import glob
from os.path import isfile


def iterate_patterns(file_glob_pattern: list[str]) -> typing.Generator[str, None, None]:
    for pattern in file_glob_pattern:
        for file in glob(pattern, recursive=True):
            if isfile(file):
                yield file
