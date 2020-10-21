#!/usr/bin/env python3

"""
logginer.py         - create a project python with all the required files and folder
Author              - 0pb
Link                - https://github.com/0pb/
LICENSE GNU V3
"""

# libraries
import logging
from functools import wraps

# --------------------------------------------------------------------------------------------


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\033[36m"
    yellow = "\033[33m"
    red = "\033[31m"
    bold_red = "\033[7;31;31m"
    reset = "\033[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # format = "[%(filename)s:%(lineno)s %(funcName)15s() ] %(message)s"
    formating_1 = "%(filename)12s"
    formating_2 = "%(levelname)8s %(funcName)16s()"
    format_end = "%(message)s"

    FORMATS = {
        logging.DEBUG: f"[ {grey}{formating_1} {formating_2}{reset} ] {format_end}",
        logging.INFO: f"[ {grey}{formating_1} {formating_2}{reset} ] {format_end}",
        logging.WARNING: f"[ {yellow}{formating_1} {formating_2}{reset} ] {format_end}",
        logging.ERROR: f"[ {red}{formating_1} {formating_2}{reset} ] {format_end}",
        logging.CRITICAL: f"[ {bold_red}{formating_1} {formating_2}{reset} ] {format_end}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def set_logging(name, base_level):
    logging.root.setLevel(base_level)
    logger = logging.getLogger(name)
    logger.setLevel(base_level)

    ch = logging.StreamHandler()
    ch.setLevel(base_level)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    return logger


# @logginer.logger_show(__name__)
def logger_show(name):
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(name)
            save_level = logger.level

            # need to change every handle, root and the logger for some reason
            logger.handlers[0].setLevel(logging.NOTSET)
            logging.root.setLevel(logging.NOTSET)
            logger.setLevel(logging.NOTSET)

            res = func(*args, **kwargs)

            logger.setLevel(save_level)
            logging.root.setLevel(save_level)
            logger.handlers[0].setLevel(save_level)

            return res
        return wrapper
    return wrap


# @logginer.logger_suppress(__name__)
def logger_suppress(name):
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(name)
            save_level = logger.level

            logger.handlers[0].setLevel(60)
            logging.root.setLevel(60)
            logger.setLevel(60)

            res = func(*args, **kwargs)

            logger.setLevel(save_level)
            logging.root.setLevel(save_level)
            logger.handlers[0].setLevel(save_level)

            return res
        return wrapper
    return wrap


"""
def indentation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        for g in range(wrapper.count):
            print("  ", end='')
        return res
    wrapper.count = 0
    return wrapper
"""