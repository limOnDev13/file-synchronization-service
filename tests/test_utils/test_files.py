"""Tests for src.utils.files.py."""

import os.path
import random
from string import ascii_letters
from typing import List, Tuple

import pytest

from src.utils.files import search_files


def test_search_files(not_empty_dir: Tuple[str, List[str]]) -> None:
    """Test the search_files function on an existing directory with files."""
    dir_path, file_paths = not_empty_dir

    for file, found_file in zip(sorted(file_paths), sorted(search_files(dir_path))):
        assert file == found_file
    assert len(file_paths) == len(list(search_files(dir_path)))


def test_search_files_with_empty_dir(empty_dir: str) -> None:
    """Test the search_files function on an empty directory."""
    assert 0 == len(list(search_files(empty_dir)))


def test_search_files_in_not_existing_dir() -> None:
    """Test the search_files function on a non-existent directory."""
    random_dir_name = "".join(random.choices(ascii_letters, k=random.randint(5, 10)))
    dir_path: str = os.path.join(os.path.abspath("."), random_dir_name)
    while os.path.exists(dir_path):
        random_dir_name = "".join(
            random.choices(ascii_letters, k=random.randint(5, 10))
        )
        dir_path = os.path.join(os.path.abspath("."), random_dir_name)

    with pytest.raises(FileNotFoundError):
        list(search_files(dir_path))
