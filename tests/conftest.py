"""A module with test fixtures."""
import os
import random
from typing import List, Tuple

import pytest


@pytest.fixture()
def not_empty_dir() -> Tuple[str, List[str]]:
    """Fixture for getting paths to a directory and files inside it."""
    dir_name: str = "not_empty_dir"
    dir_path: str = os.path.join(os.path.abspath(""), dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    filename_template: str = "not_empty_file{}.txt"
    files: List[str] = list()
    for i in range(random.randint(1, 10)):
        file_path: str = os.path.join(dir_path, filename_template.format(i))
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(filename_template)
            files.append(file_path)

    yield dir_path, files

    for file_path in files:
        os.remove(file_path)
    os.rmdir(dir_path)


@pytest.fixture()
def empty_dir() -> str:
    """Fixture for getting path to an empty directory."""
    dir_name: str = "empty_dir"
    dir_path: str = os.path.join(os.path.abspath(""), dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    yield dir_path

    os.rmdir(dir_path)
