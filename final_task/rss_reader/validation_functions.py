""" Module of validation functions.

    Functions:
    check_url(com_line_args, logger) -> True
    check_internet_connection(logger) -> True
    check_emptiness(news_collection, logger) -> True
    check_version_arg(com_line_args, logger) -> True/False
    check_limit_arg(news_collection, com_line_args, logger) -> limit (int)
    check_date_arg(com_line_args, logger) -> True/False   """

import requests
from urllib.request import Request, urlopen
from urllib.error import URLError
from exceptions import Error, EmptyCollectionError


def check_url(com_line_args, logger):
    """ Check URL function. """
    try:
        req = Request(com_line_args.source)
        logger.info("Checking url.")
        response = urlopen(req)
    except ValueError:
        logger.error("Invalid URL.")
        raise Error("Please, check your URL.")
    except URLError as e:
        if hasattr(e, "reason"):
            logger.error(f"Failed to reach a server. Reason: {e.reason}.")
            raise Error("Please, check your internet connection and your URL.")
        elif hasattr(e, 'code'):
            logger.error("The server couldn\'t fulfill the request. "
                         f"Error code: {e.code}")
            raise Error("Service problem.")
    else:
        return True


def check_internet_connection(logger):
    """ Check internet connection function. """
    try:
        logger.info("Checking internet connection.")
        response = requests.get("http://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        logger.error("No internet connection.")
        raise Error("Please, check your internet connection.")


def check_emptiness(news_collection, logger):
    """ Function for checking news availability in news collection. """
    logger.info("Checking news collection emptiness.")
    if not (news_collection["feed"] and news_collection["entries"]):
        logger.error("Empty RSS-feed.")
        raise Error("Please, check URL.")
    else:
        return True


def check_version_arg(com_line_args, logger):
    """ Check --version argument function. """
    if com_line_args.version:
        logger.info("View program version.")
        print("rss_reader.py 1.0")
        return True
    else:
        return False


def check_limit_arg(com_line_args, logger):
    """ Check --limit argument function. """
    if com_line_args.limit or com_line_args.limit == 0:
        return True
    if com_line_args.limit < 0:
        logger.error("Command line argument limit is invalid.")
        raise EmptyCollectionError("Command line argument limit should not be negative.")


def check_date_arg(com_line_args, logger):
    """ Check --date argument function. """
    if com_line_args.date:
        logger.info("Checking date argument.")
        return True
    else:
        return False
