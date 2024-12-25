"""A module for working with files."""

import os
from typing import Iterator


def search_files(init_dir: str, depth: int = 0) -> Iterator[str]:
    """
    Find all the files in the directory recursively.

    :param init_dir: The directory where the search takes place.
    :param depth: The depth of recursion.
    :return: An iterator that returns the full file paths.
    """
    for name in os.listdir(init_dir):
        path = os.path.join(init_dir, name)
        if os.path.isdir(path) and depth > 0:
            for filepath in search_files(path, depth - 1):
                yield filepath
        elif os.path.isfile(path):
            yield path
