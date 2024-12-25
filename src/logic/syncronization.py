"""The module responsible for file synchronization."""

import os.path
from logging import getLogger
from threading import Thread
from typing import List, Set
from urllib.parse import unquote

from src.clouds.cloud import Cloud
from src.utils.files import search_files

logger = getLogger("main.sync")


def synchronize(cloud: Cloud, init_dir: str) -> None:
    """Synchronize local and remote dirs."""
    logger.info("Start synchronizing...")

    local_files: Set[str] = set(search_files(init_dir))
    remote_files: Set[str] = {unquote(data["name"]) for data in cloud.get_info()}
    differ = remote_files - {os.path.basename(local_file) for local_file in local_files}

    logger.debug("Updating files...")
    threads: List[Thread] = list()
    for file_path in local_files:
        t: Thread = Thread(target=cloud.reload, args=(file_path,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    logger.debug("Deleting unnecessary files...")
    threads.clear()
    for deleted_filename in differ:
        t = Thread(target=cloud.delete, args=(deleted_filename,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    logger.info("Done")
