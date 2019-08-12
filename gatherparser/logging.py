import sys
import logging


def get_loggger(module_name: str, filename: str = "logfile.log") -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
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
    # File handler
    file_handler = logging.FileHandler(filename=filename, encoding="utf8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s [%(name)s] %(message)s'))
    logger.addHandler(file_handler)

    return logger
