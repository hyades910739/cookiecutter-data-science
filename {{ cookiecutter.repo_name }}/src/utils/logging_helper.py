import logging
from datetime import datetime


def get_logger(name="src", filename=None, add_time_suffix=True, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(threadName)s][%(thread)x]-%(name)-8s-%(funcName)-10s-%(levelname)-5s-%(lineno)d: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if filename is not None:
        if add_time_suffix:
            now = datetime.now().strftime(format="%Y%m%d-%H%M%S")
            filename = "_".join([filename, now])
        file_handler = logging.FileHandler("test.log")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
