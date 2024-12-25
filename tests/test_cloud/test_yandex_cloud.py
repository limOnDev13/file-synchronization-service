"""Module with tests for YandexCloud."""
import os.path
import random
from string import ascii_letters
from typing import List, Tuple

import pytest

from src.clouds.yandex_cloud import YandexCloud


def test_load_file(not_empty_dir: Tuple[str, List[str]], cloud: YandexCloud) -> None:
    """Test loading file on yandex disk."""
    _, file_paths = not_empty_dir

    try:
        for path in file_paths:
            cloud.reload(path)
    except Exception as exc:
        pytest.fail(str(exc))


def test_load_not_existing_file(cloud: YandexCloud) -> None:
    """Test loading non-existing file on yandex disk."""
    not_existing_filename: str = (
        "".join(random.choices(ascii_letters, k=random.randint(5, 10))) + ".txt"
    )

    while os.path.exists(not_existing_filename):
        not_existing_filename = (
            "".join(random.choices(ascii_letters, k=random.randint(5, 10))) + ".txt"
        )

    with pytest.raises(FileNotFoundError):
        cloud.load(not_existing_filename)


def test_load_file_in_not_existing_dir_on_disk(
    cloud: YandexCloud, not_empty_dir: Tuple[str, List[str]]
) -> None:
    """Test uploading a file to a non-existent folder on a remote disk."""
    _, file_paths = not_empty_dir
    path = file_paths[0]

    cloud.remote_dir_path = "".join(
        random.choices(ascii_letters, k=random.randint(10, 20))
    )

    with pytest.raises(ValueError):
        cloud.reload(path)


def test_delete_file_on_disk(
    cloud: YandexCloud, not_empty_dir: Tuple[str, List[str]]
) -> None:
    """Test file deletion on yandex disk."""
    _, file_paths = not_empty_dir
    path = file_paths[0]

    try:
        cloud.reload(path)
        cloud.delete(os.path.basename(path))
    except Exception as exc:
        pytest.fail(str(exc))


def test_delete_not_existing_file_on_disk(cloud: YandexCloud) -> None:
    """Test deleting non-existing file from yandex disk."""
    not_existing_filename: str = (
        "".join(random.choices(ascii_letters, k=random.randint(20, 30))) + ".txt"
    )

    with pytest.raises(ValueError):
        cloud.delete(not_existing_filename)
