import logging


def functions_log(function):
    def wrapper(*args, **kwargs):
        logging.info(f'start function: {function.__name__}')
        result = function(*args, **kwargs)
        logging.info(f'end function: {function.__name__}')
        return result

    return wrapper
