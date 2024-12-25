"""A module for configuring and launching the application."""

import logging.config
import time
from logging import getLogger

from clouds.cloud import Cloud
from clouds.yandex_cloud import YandexCloud
from config.env_config import Config
from config.log_config import log_config
from src.logic.syncronization import synchronize

logging.config.dictConfig(log_config)
logger = getLogger("main")


def main():
    """Configure and launch the app."""
    logger.debug("Starting app...")
    config: Config = Config()
    cloud: Cloud = YandexCloud(
        token=config.token,
        remote_dir_path=config.remote_dir_path,
    )

    while True:
        synchronize(cloud=cloud, init_dir=config.target)
        time.sleep(config.delay)


if __name__ == "__main__":
    main()
