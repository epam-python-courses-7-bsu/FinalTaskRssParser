"""Contain checking functions"""

import requests
import logging
import sys
import classes.exceptions as exc

def check_internet_connection(logger):
    """Check if network connection is avaliable"""
    try:
        logger.info("Checking internet connection...")
        requests.get('https://www.google.com/', timeout=1)
        return True
    except requests.ConnectionError:
        raise exc.InternetConnectionError("No internet access")


def check_verbose(command_line_args):
    """If vebose argument is True, set logging to info level"""

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                        stream=sys.stdout,
                        level=logging.INFO
                        )
    logger = logging.getLogger("rss_reader_logger")
    if command_line_args.verbose:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    return logger


def check_feed_status(feed):
    """Check HTTP status code"""

    try:
        status = feed.status
        if 500 > status >= 400:
            raise exc.GettingFeedError("Client error – the request contains bad syntax or cannot be fulfilled.")
        elif 600 > status >= 500:
            raise exc.GettingFeedError("Server error – the server failed to fulfill an apparently valid request.")
        else:
            return feed
    except AttributeError:
        raise exc.UrlError("Url is not valid")


def check_news_collection(news_collection, logger):
    """Check if news_collection is not empty"""
    if not news_collection:
        raise exc.FeedXmlError("Parsed xml is not valid")
    else:
        logger.info("Successful collected.")
