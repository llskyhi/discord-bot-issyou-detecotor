#!/usr/bin/env python
# encoding=utf-8
import sys
import os
import logging
import logging.config
import pathlib
import yaml

import dotenv

import issyou_detector.version
from issyou_detector import IssyouDetector
from issyou_detector.datastore import ChannelRegisterRepo
from issyou_detector.datastore.impl import InMemoryChannelRegisterRepo
from issyou_detector.datastore.impl import JsonChannelRegisterRepo

LOGGER = logging.getLogger(__name__)

def _configure_logging() -> None:
    log_config_file_path = pathlib.Path(__file__).parent.joinpath("logging-config.yaml")
    log_config: dict
    try:
        with log_config_file_path.open("r", encoding="utf-8") as log_config_file:
            log_config = yaml.safe_load(
                stream=log_config_file,
            )
        logging.config.dictConfig(log_config)
    except FileNotFoundError as error:
        _configure_logging_minimal()
        LOGGER.info(f"Expected logging config file ({log_config_file_path}) does not exist.")
    except Exception as error:
        _configure_logging_minimal()
        LOGGER.warning(f"Failed to load logging configuration from file {log_config_file_path}.", exc_info=error)
    LOGGER.info("Finished configuring logging.")

def _configure_logging_minimal() -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": "DEBUG",
            "handlers": (
                "console",
            ),
        },
        "formatters": {
            "minimal": {
                "format": "%(asctime)s (%(relativeCreated)3d) %(levelname)8s| (%(name)s) %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "minimal",
                "level": "DEBUG",
                "stream": sys.stdout,
            },
        },
    }
    logging.config.dictConfig(logging_config)
    LOGGER.info("Using minimal logging configuration.")

if __name__ == "__main__":
    dotenv.load_dotenv(
        verbose=True,
        override=True,
    )

    print("Configuring logging...")
    _configure_logging()

    if "ISSYOU_DETECTOR_TOKEN" not in os.environ:
        LOGGER.error("Please provide the discord bot token as environment variable ISSYOU_DETECTOR_TOKEN, maybe via dotenv file.")
        exit(1)
    LOGGER.info(f"Going to run issyou-detector, version {issyou_detector.version.__version__}...")

    bot_token = os.environ["ISSYOU_DETECTOR_TOKEN"]
    data_root_path = pathlib.Path(os.environ.get("ISSYOU_DETECTOR_DATA_ROOT_PATH", "./data"))
    use_in_memory_data = "ISSYOU_DETECTOR_USE_IN_MEMORY_DATA" in os.environ

    channel_register_repo: ChannelRegisterRepo
    if use_in_memory_data:
        channel_register_repo = InMemoryChannelRegisterRepo()
    else:
        channel_register_repo = JsonChannelRegisterRepo(
            data_root_path=data_root_path,
        )

    bot = IssyouDetector(
        channel_register_repo=channel_register_repo,
    )

    bot.run(
        token=bot_token,
        log_handler=None,
    )
