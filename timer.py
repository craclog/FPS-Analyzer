import time
from logger import setup_logger

logger = setup_logger()

def timer_decorator(func):
    """ A decorator that logs the runtime of a function. """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.debug("Finished %r in %.4f secs", func.__name__, run_time)
        return result
    return wrapper
