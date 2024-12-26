"""A module for getting configuration parameters from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Delay(object):
    """Config for delay."""

    days: int = int(os.getenv("DAYS", 0))
    hours: int = int(os.getenv("HOURS", 0))
    minutes: int = int(os.getenv("MINUTES", 0))
    seconds: int = int(os.getenv("SECONDS", 0))

    def __init__(self):
        if (
            self.days == 0
            and self.hours == 0
            and self.minutes == 0
            and self.seconds == 0
        ):
            self.minutes = 1


@dataclass
class Config(object):
    """Config class."""

    token: str = os.getenv("TOKEN", "")
    target: str = os.getenv("TARGET", ".")
    remote_dir_path: str = os.getenv("REMOTE_DIR_PATH", "")

    def __init__(self):
        self.delay = Delay()
