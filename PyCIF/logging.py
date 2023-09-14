"""
Logging objects shared by entire package
"""
import logging

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


def get_logger(name):
    """
    Get logger and configure it to use stream_handler and formatter
    """
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)
    log.propagate = False
    return log
