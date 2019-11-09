""" Module of validation functions.

    Functions:
    check_url(com_line_args, logger) -> True
    check_internet_connection(com_line_args, logger) -> True
    check_emptiness(news_collection, logger) -> True
    check_version_arg(com_line_args, logger) -> None
    check_limit_arg(news_collection, com_line_args, logger) -> limit (int) """

import requests
from urllib.request import Request, urlopen
from urllib.error import URLError


def check_url(com_line_args, logger):
    """ Check URL function. """
    req = Request(com_line_args.source)
    try:
        logger.info("Checking url.")
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, "reason"):
            logger.error(f"Failed to reach a server. ")
            print("Please, check your URL.")
            exit()
        elif hasattr(e, 'code'):
            print("The server couldn\'t fulfill the request.")
            print('Error code: ', e.code)
    else:
        return True


def check_internet_connection(com_line_args, logger):
    """ Check internet connection function. """
    try:
        logger.info("Checking internet connection.")
        response = requests.get("http://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        logger.error("No internet connection. "
                     "Check your internet connection")
        answer = input("Would you like to try again? (Y/n): ")
        if answer.lower() == 'y':
            check_internet_connection(com_line_args, logger)
        else:
            exit()


def check_emptiness(news_collection, logger):
    """ Function for checking news availability in news collection. """
    logger.info("Checking news collection emptiness.")
    if not (news_collection["feed"] and news_collection["entries"]):
        logger.error("Empty RSS-feed. Please, check URL.")
        exit()
    else:
        return True


def check_version_arg(com_line_args, logger):
    """ Check --version argument function. """
    if com_line_args.version:
        logger.info("View program version.")
        print("rss_reader.py 1.0")
        exit()


def check_limit_arg(news_collection, com_line_args, logger):
    """ Check --limit argument function.

        Analyzes the received value and makes it valid for correct program work. """
    if com_line_args.limit or com_line_args.limit == 0:
        limit = com_line_args.limit
    else:
        limit = len(news_collection["entries"])
    if limit < 0:
        logger.warning("Command line argument limit is invalid.")
        print("Command line argument limit is invalid. "
              "It should not be negative.")
        com_line_args.limit = int(input("Please, enter a valid value:"))
        check_limit_arg(news_collection, com_line_args, logger)

    return limit
