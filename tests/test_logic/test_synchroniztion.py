"""Tests for module src.logic.synchronization."""

from typing import List, Tuple

import pytest

from src.clouds.yandex_cloud import YandexCloud
from src.logic.syncronization import synchronize


def test_synchronize(not_empty_dir: Tuple[str, List[str]], cloud: YandexCloud) -> None:
    """Test func synchronize."""
    dir_path, _ = not_empty_dir

    try:
        synchronize(cloud, init_dir=dir_path)
    except Exception as exc:
        pytest.fail(str(exc))
