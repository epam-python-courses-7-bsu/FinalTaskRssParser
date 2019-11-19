import logging


def log_decore(fn):
    def wrapper(*args, **kwargs):
        logging.info(f"function \"{fn.__name__}\"Run function")
        res = fn(*args, **kwargs)
        logging.info(f"function \"{fn.__name__}\"Stop function")
        return res

    return wrapper
