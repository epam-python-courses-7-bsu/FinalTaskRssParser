"""Contain checking functions

Functions
---------
check_internet_connection(logger) -> Bool
    Check if network connection is avaliable
--------------------------------------------
check_version_argument(command_line_args) -> None
    If version argument, print version and exit
--------------------------------------------
check_verbose(command_line_args): -> logger
    If vebose argument is True, set logger to info level
--------------------------------------------
check_feed_status(feed, logger)
    Check HTTP status code
--------------------------------------------
def check_news_collection(news_collection, logger) -> news_collection
    Check if news_collection is not empty
"""

import requests
import logging
import sys


def check_internet_connection(logger):
    """Check if network connection is avaliable"""
    try:
        logger.info("Checking internet connection...")
        requests.get('http://216.58.192.142', timeout=1)
        return True
    except requests.ConnectionError:
        logger.warning("Check internet connection")
        # Ask user is he want to proceed
        answer = input("Do you want to proceed? (Y/n): ")
        if answer.lower() == 'y':
            check_internet_connection(logger)
        else:
            exit()


def check_version_argument(command_line_args):
    """If version argument, print version and exit"""
    if command_line_args.version:
        print("rss_reader.py 1.0")
        exit()


def check_verbose(command_line_args):
    """If vebose argument is True, set logging to info level"""

    logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s',
                        stream=sys.stdout,
                        level=logging.INFO
                        )
    logger = logging.getLogger("rss_reader_logger")
    if command_line_args.verbose:
        logger.setLevel(level=logging.INFO)
        return logger
    else:
        logger.setLevel(level=logging.WARNING)
        return logger


def check_feed_status(feed, logger):
    """Check HTTP status code"""

    if feed.status:
        if feed.status == 404:
            logger.error("Page not found")
            exit()
        else:
            return feed
    else:
        logger.error("Url is not valid")
        exit()


def check_news_collection(news_collection, logger):
    """Check if news_collection is not empty"""
    if not news_collection:
        logger.error("Feeds hadn't got! Please, check if you use valid url!")
        exit()
    else:
        logger.info("Successful collected.")
