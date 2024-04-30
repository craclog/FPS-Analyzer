import logging

def setup_logger():
    logger = logging.getLogger("FPS Analyzer")

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(funcName)s:%(lineno)d - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger
