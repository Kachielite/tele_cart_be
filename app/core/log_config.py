# logging_config.py
import logging.config
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {  # Uvicorn logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {  # Uvicorn error logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {  # Uvicorn access logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {  # Your app logger (adjust this based on your app's name)
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
