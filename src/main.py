"""A module for configuring and launching the application."""

import logging.config
from logging import getLogger

from config.log_config import log_config

logging.config.dictConfig(log_config)
logger = getLogger("main")


def main():
    """Configure and launch the app."""
    logger.debug("Starting app...")
