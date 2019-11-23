#!/usr/bin/env python3.8

import requests

import rss_exceptions as er


def check_internet_connection(logger):
    """
    Check the internet connection
    """
    try:
        logger.info("Check the Internet connection")
        requests.get('https://www.google.com/', timeout=1)
    except requests.exceptions.ConnectionError:
        raise er.InternetConnectionError("No connection to the Internet.")


def check_url_availability(cmd_args, logger):
    """
    Check the URL availability
    """
    url = cmd_args.source
    try:
        response = requests.get(url)
        logger.info('Check the Internet connection.')
    except Exception:
        raise er.UnreachableURLError("No connection to the Internet.")
    else:
        logger.info('Connection established.')


def check_response_status_code(cmd_args, logger):
    """
    Check if the response status code is 200: OK
    """
    url = cmd_args.source
    response = requests.get(url)
    if response.status_code != 200:
        raise er.URLResponseError(f'Bad response status code {str(response.status_code())}.')

    logger.info('The response status code is 200: OK.')


def check_limit_value(limit, logger):
    """
    Check if received limit value is valid
    """
    if limit and limit < 0:
        logger.info(f'Check if the received limit value = {limit} is valid.')
        raise er.LimitSignError(f'Limit value must be positive.')

    logger.info(f"The 'limit' variable is assigned the total amount of received news {limit}.")


def check_news_collection(news_collection, logger):
    """
    Check news_collection is not empty
    """
    if not news_collection:
        raise er.FeedError("Link doesn't contain any news.")

    logger.info("News was collected successfully.")
