from typing import Dict, Any


log_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "[%(asctime)s] %(message)s",
        },
        "console": {
            "format": "[%(levelname)s] [%(asctime)s] %(module)s.%(funcName)s | %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "file",
            "filename": "logfile.log",
            "backupCount": 3,
            "when": "d",
            "interval": 10,
            "encoding": "utf-8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
}
