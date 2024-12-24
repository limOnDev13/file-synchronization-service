import os
from typing import Iterator


def search_files(init_dir: str, depth: int = 0) -> Iterator[str]:
    for name in os.listdir(init_dir):
        path = os.path.join(init_dir, name)
        if os.path.isdir(path) and depth > 0:
            for filepath in search_files(path, depth - 1):
                yield filepath
        elif os.path.isfile(path):
            yield path
