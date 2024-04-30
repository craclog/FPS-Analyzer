import logging

def setup_logger():
    logger = logging.getLogger("fps_analyzer")

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(funcName)s:%(lineno)d - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger
