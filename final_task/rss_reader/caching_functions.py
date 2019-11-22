"""  Module of caching functions.

      Functions:
      cache_news(news_collection, logger) -> None
      get_cached_news(com_line_args, logger) -> cached_news_collection   """

import shelve
from os import path

from validation_functions import check_limit_arg
from exceptions import EmptyFileError, EmptyCollectionError

DIRECTORY = path.abspath(path.dirname(__file__))


def cache_news(news_collection, logger):
    """ Caching news function. """
    logger.info("Collecting news to cache file.")
    with shelve.open(path.join(DIRECTORY, '.cache_rss_news')) as news_dict:
        for news in news_collection["entries"]:
            hash_date = news.date
            news_dict[hash_date] = news
    logger.info("News was cached successfully.")


def get_cached_news(com_line_args, logger):
    logger.info("Getting cache news.")
    date = com_line_args.date
    source = com_line_args.source
    check_limit_arg(com_line_args, logger)

    cached_news_collection = []

    with shelve.open(path.join(DIRECTORY, '.cache_rss_news')) as news_dict:
        if not news_dict:
            raise EmptyFileError("Cache file is empty. Please, retrieve news from internet. ")

        limit = min(com_line_args.limit, len(news_dict))

        if source:
            for hash_date_key in news_dict:
                if date in hash_date_key:
                    news = news_dict[hash_date_key]
                    if source == news.source:
                        cached_news_collection.append(news)
        else:
            for hash_date_key in news_dict:
                if date in hash_date_key:
                    news = news_dict[hash_date_key]
                    cached_news_collection.append(news)

    if not cached_news_collection:
        if source:
            raise EmptyCollectionError("There are no news in cache file on specified date and source.")
        else:
            raise EmptyCollectionError("There are no news in cache file on specified date.")

    else:
        logger.info("Successfully get news from cache.")
        return cached_news_collection[:limit]
