import logging
import sys


class logger:
    '''
    Uses standart logging lib to implement custom logger that can be used
    within whole project
    '''
    is_log_on = False
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
    @staticmethod
    def log(msg):
        if logger.is_log_on:
            logging.debug(msg)
