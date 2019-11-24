"""This module creates logs, writes logs, reads logs."""

import logging
import os
import news

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

JOURNAL_LOG = 'logJournal.log'
DIRECTORY = os.path.join(THIS_DIRECTORY, JOURNAL_LOG)

args = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=DIRECTORY, format=args, level=logging.INFO, filemode='a+')


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

    with open(DIRECTORY, 'r') as log:
        for line in log:
            if 'INFO - News was written to local storage: url -' in line:
                """
                This code cuts line into two slices:
                    url - slice with link
                    info - slice with information
                Since lines has the same pattern, the slices will be the same
                """
                url = line[73:]
                info = line[0:66]
                print(info)
                print('Link for the news: ' + url, end='')
                news.news_log_add(url)
            else:
                print(line, end='')


def log_prepare() -> dict:
    """This function prepares log journal for conversion"""
    log_journal = dict()
    counter = 0

    with open(DIRECTORY, 'r') as log:
        for line in log:
            log_journal[counter] = line
            counter += 1

    return log_journal


def log_print():
    """This function logs print operation"""

    logging.info('Log journal printed')


def log_news_store(url: str):
    """This function logs news storage operation"""

    logging.info('News was written to local storage: url - '+url)


def log_news_print():
    """This function logs news print from storage"""

    logging.info('News was printed from storage')


def log_news_print_err():
    """This function logs the error if news is not in storage"""

    logging.error('The news is not in storage')


def log_news_filenotfound():
    """This function logs if local news storage is not found"""

    logging.error('Local news storage is not found')


def log_invalid_arguments(args: str):
    """This function logs invalid arguments"""

    logging.error('Arguments not valid: ' + args)


def log_news_limit(limit: int):
    """This function logs when news limit is reached"""

    logging.info('News limit for print is reached: ' + str(limit))


def log_news_copycat(url: str):
    """This function logs attempt of writing duplicate news"""

    logging.warning('Attempt to write duplicate news: url - ' + url)


def log_news_local_storage_pdf():
    """This function logs the conversion from local storage"""

    logging.info('News from local storage vere converted to pdf')


def log_news_pdf():
    """This function logs the conversion from rss feed"""

    logging.info('News from rss feed were converted to pdf')


def log_news_local_storage_html():
    """This function logs the conversion from local storage"""

    logging.info('News from local storage vere converted to html')


def log_news_html():
    """This function logs the conversion from rss feed"""

    logging.info('News from rss feed were converted to html')


def log_log_pdf():
    """This function logs the conversion of log journal to pdf"""

    logging.info('Log journal was converted to pdf')


def log_log_html():
    """This function logs the conversion of log journal to html"""

    logging.info('Log journal was converted to html')


def print_log_verbose_pdf():
    """This function prints"""

    str_1 = 'News from rss feed were converted to pdf'
    str_2 = 'News from local storage vere converted to pdf'

    with open(DIRECTORY, 'r') as log:
        for line in log:
            if (str_1 in line) or (str_2 in line):
                print(line, end='')


def print_log_verbose_html():
    """This function prints"""

    str_1 = 'News from rss feed were converted to html'
    str_2 = 'News from local storage vere converted to html'

    with open(DIRECTORY, 'r') as log:
        for line in log:
            if (str_1 in line) or (str_2 in line):
                print(line, end='')
