"""This module creates logs, writes logs, reads logs."""

import logging
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

journalLog = 'logJournal.log'
directory = os.path.join(this_directory, journalLog)

args = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=directory, format=args, level=logging.INFO, filemode='a+')


def new_session():
    """This function logs the beginning of a new session"""

    logging.info('+++++ STARTING NEW SESSION +++++')


def end_session():
    """This function ends the session"""

    logging.info('+++++ ENDING THE SESSION +++++')


def log_url(name: str):
    """This function logs url"""

    logging.info('Initial url success: ' + name)


def log_connection(name: str):
    """This function logs connection"""

    logging.info('Server connection success: ' + name)


def log_rss(name: str):
    """This function logs RSS URL"""

    logging.info('RSS connection success: ' + name)


def log_wrong_url(name: str):
    """This function logs the wrong url"""

    logging.warning('Potentially wrong URL: ' + name)


def log_connection_failed(name: str):
    """This function logs the failed connection"""

    logging.error('Cannot create connection with server: ' + name)


def log_wrong_rss(name: str):
    """This function logs wrong RSS URL"""

    logging.warning('Cannot get RSS feed: ' + name)


def log_init_args(name: str):
    """This function logs initial arguments"""

    logging.info('Initial arguments: %s', name)


def log_err_init_args(name: str):
    """This function logs wrong initial arguments"""

    logging.error('Wrong initial arguments: %s', name)


def log_err_exit():
    """This function logs the error exit"""

    logging.error('+++++ ERROR EXIT +++++')


def print_log():
    """This function prints"""

    with open(directory, 'r') as log:
        for line in log:
            print(line, end='')


def log_print():
    """This function logs print operation"""

    logging.info('Log journal printed')


