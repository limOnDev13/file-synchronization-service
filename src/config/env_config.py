"""A module for getting configuration parameters from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config(object):
    """Config class."""

    token: str = os.getenv("TOKEN", "")
    target: str = os.getenv("TARGET", ".")
    remote_dir_path: str = os.getenv("REMOTE_DIR_PATH", "")
    delay: int = int(os.getenv("DELAY", 60))
