import json
import logging.config
from logging import getLogger
from typing import List
from urllib.parse import unquote

from utils.files import search_files
from config.env_config import Config
from config.log_config import log_config
from clouds.yandex_cloud import YandexCloud
from clouds.cloud import Cloud

logging.config.dictConfig(log_config)
logger = getLogger("main")


def main():
    logger.debug("Starting app...")
    config: Config = Config()
