#!/usr/bin/env python3.8

import itertools
import shelve
from os import path

from rss_exceptions import SpecifiedDayNewsError, EmptyCacheError
from validator import check_limit_value


DIRECTORY = path.abspath(path.dirname(__file__))


def cache_news(parsed_news, logger):
    """
    Cache news in 'feeds_cache' file.
    """
    logger.info('Trying to cache news into a file')
    with shelve.open(path.join(DIRECTORY, '.feeds_cache')) as cache:
        for new in parsed_news:
            date = new['date']
            cache[date] = new

    logger.info('News was cached successfully.')


def get_cached_news(cmd_args, logger):
    """
    Extract news from the cache for a specified day.
    """
    check_limit_value(cmd_args.limit, logger)
    logger.info("Get started fetching cached news if exists.")

    with shelve.open(path.join(DIRECTORY, '.feeds_cache')) as cache:
        if not cache:
            raise EmptyCacheError('Cache is empty. Please, retrieve data from internet.')

        limit = cmd_args.limit or len(cache)
        all_news = []

        for new in itertools.islice(make_news_collection(cmd_args, cache), 0, limit):
            all_news.append(new)

    if not all_news or all_news == [None]:
        logger.info('No entries on the specified day (and url, if assigned) in the cache.')
        raise SpecifiedDayNewsError('On the specified day there are no entries in the cache.')

    logger.info('News was extracted from the cache successfully.')
    return all_news


def make_news_collection(cmd_args, cache):
    """
    Iterate the cache with required key 'data' and 'url', if specified.
    """
    for key_date in cache:
        if cmd_args.date in key_date:
            news_date = cache[key_date]
            if cmd_args.source == news_date['feed_url']:
                yield news_date
            elif not cmd_args.source:
                yield news_date
