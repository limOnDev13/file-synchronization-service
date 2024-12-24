from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config(object):
    token: str = os.getenv("TOKEN")
    target: str = os.getenv("TARGET")
    remote_dir_path: str = os.getenv("REMOTE_DIR_PATH")
