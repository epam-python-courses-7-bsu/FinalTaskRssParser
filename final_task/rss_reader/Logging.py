import logging


def logging_decorator(func):
    """decorator for print logs in stdout"""
    def wrapper(*args, **kwargs):
        logging.info(f"function \"{func.__name__}\" started")
        res = func(*args, **kwargs)
        logging.info(f"function \"{func.__name__}\" finished")
        return res
    return wrapper
