import typing
from glob import glob
from os.path import isfile


def iterate_patterns(file_glob_pattern: list[str]) -> typing.Generator[str, None, None]:
    """
    Iterate all files in the given glob patterns, ignoring folders
    :param file_glob_pattern: Patterns to apply to glob
    :return: Iterator emitting file names
    """
    for pattern in file_glob_pattern:
        for file in glob(pattern, recursive=True):
            if isfile(file):
                yield file
