#!/usr/bin/env python3.8

import requests

from rss_exceptions import FeedError


def check_the_connection(cmd_args, logger):
    """
    Check the internet connection
    """
    url = cmd_args.source
    try:
        requests.get(url, timeout=5)
        logger.info('Check the Internet connection.')
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
    ) as error:
        logger.error(f'URL {url} is unreachable.' + error)
        raise Exception(f'URL {url} is unreachable.')
    else:
        logger.info('Connection established.')


def check_response_status_code(cmd_args, logger):
    """
    Check if the response status code is 200: OK
    """
    url = cmd_args.source
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Bad response status code {str(response.status_code)}')

    logger.info('The response status code is 200: OK.')


def check_limit_value(limit, logger):
    """
    Check if received limit value is valid
    """
    if limit and limit < 0:
        logger.info(f'Check if the received limit value = {limit} is valid.')
        raise ValueError(f'Limit value must be positive.')

    logger.info(f"The 'limit' variable is assigned the total amount of received news {limit}.")


def check_news_collection(news_collection, logger):
    """
    Check news_collection is not empty
    """
    logger.info('')

    if not news_collection:
        raise FeedError("Link doesn't contain any news.")

    logger.info("News was collected successfully.")
