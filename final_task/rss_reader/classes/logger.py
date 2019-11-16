import logging
import sys


class logger:
    '''
    Uses standart logging lib to implement custom logger that can be used
    within whole project
    '''
    is_log_on = False
    logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
    @staticmethod
    def log(msg):
        '''
        Receives message and prints it into stdout if logging is turned on
        '''
        if logger.is_log_on:
            logging.debug(msg)
