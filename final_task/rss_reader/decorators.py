import logging


def functions_log(f):
    def wrapper(*args, **kwargs):
        logging.info(f'start function: {f.__name__}')
        result = f(*args, **kwargs)
        logging.info(f'end function: {f.__name__}')
        return result

    return wrapper
