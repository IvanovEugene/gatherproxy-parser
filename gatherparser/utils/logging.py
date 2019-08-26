# encoding: utf-8
# TODO: migrate to aiologger
import logging


class Logging:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.propagate = True

        return logger
