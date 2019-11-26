#!/usr/bin/env python3.8
"""Module contains functions for validation utility work"""

import requests

from logger import LOGGER
import rss_exceptions as er


def check_internet_connection():
    """
    Check the internet connection
    """
    try:
        LOGGER.info("Check the Internet connection")
        requests.get('https://www.google.com/', timeout=1)
    except requests.exceptions.ConnectionError:
        raise er.InternetConnectionError("No connection to the Internet.")
    return True


def check_url_availability(cmd_args):
    """
    Check the URL availability
    """
    if cmd_args.source:
        url = cmd_args.source
        try:
            requests.get(url)
            LOGGER.info('Check the URL availability.')
        except Exception:
            raise er.UnreachableURLError("URL is invalid.")
        else:
            LOGGER.info('URL is valid. Connection established.')
            return True
    else:
        raise er.UndefinedURL('URL is required')


def check_response_status_code(cmd_args):
    """
    Check if the response status code is not greater than 400
    """
    try:
        url = cmd_args.source
        response = requests.get(url)
        response.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        raise er.URLResponseError(f'Bad response status code. Use another URL.')

    LOGGER.info(f'The response status code is {response.status_code}.')
    return True


def check_limit_value(limit):
    """
    Check if received limit value is valid
    """
    if limit and limit < 0:
        raise er.LimitSignError('Limit value must be positive.')
    elif limit is None:
        LOGGER.info("Limit set to maximum news")
    else:
        LOGGER.info(f"Limit set to {limit}.")

    return True


def check_news_collection(news_collection):
    """
    Check news_collection is not empty
    """
    if not news_collection:
        raise er.FeedError("Link doesn't contain any news.")

    LOGGER.info("News collected successfully.")
    return True
