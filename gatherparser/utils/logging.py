# encoding: utf-8
# TODO: migrate to aiologger
import logging


class Logging:
    @staticmethod
    def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = True

        return logger
