#!/usr/bin/python3

import logging
import os


class Logger:
    def __init__(self) -> None:
        log_level = os.getenv("LOG_LEVEL", logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        stream = logging.StreamHandler()

        logging.getLogger("httpx").setLevel(logging.ERROR)
        logging.getLogger("pika").setLevel(logging.ERROR)
        stream.setFormatter(formatter)
        self.logger = logging.getLogger()

        self.logger.setLevel(log_level)
        self.logger.addHandler(stream)

    def debug(self, text) -> None:
        self.logger.debug(text)

    def info(self, text) -> None:
        self.logger.info(text)

    def error(self, text) -> None:
        self.logger.error(text)

    def critical(self, text) -> None:
        self.logger.critical(text)
