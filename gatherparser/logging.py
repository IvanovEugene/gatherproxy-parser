# encoding: utf-8
# TODO: migrate to aiologger
import sys
import logging


def get_logger(module_name: str) -> logging.Logger:
    # Main (module) logger
    main_logger = logging.getLogger("gatherparser")
    main_logger.setLevel(logging.INFO)
    # Concrete logger
    logger = main_logger.getChild(module_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # Stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(lambda entry: entry.levelno <= logging.INFO)
    stdout_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s [%(name)s] %(message)s'))
    logger.addHandler(stdout_handler)
    # Stderr handler
    stderr_handler = logging.StreamHandler(sys.stderr)  # stderr
    stderr_handler.addFilter(lambda entry: entry.levelno > logging.INFO)
    stderr_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s [%(name)s] %(message)s'))
    logger.addHandler(stderr_handler)

    return logger
