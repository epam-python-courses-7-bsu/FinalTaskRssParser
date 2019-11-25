"""Module for news caching in a "shelve", persistent dictionary-like object """

import shelve
from os import path
from classes.exceptions import ExtractNewsException
from classes.news_class import News


def cache_news(news_collection, logger):
    """Function collect news to database"""
    # Get path for database
    home_dir = path.expanduser('~')

    logger.info("Collecting news to database...")
    with shelve.open(path.join(home_dir, '.rss_feed')) as database:
        for news in news_collection:
            date = news.date
            database[date] = news
    logger.info("Successful collected to database")


def get_cached_news(command_line_arguments, logger):
    """Get news from database, published on date"""
    home_dir = path.expanduser('~')
    date = command_line_arguments.date
    logger.info("Getting news from database...")
    News.command_line_args = command_line_arguments
    source = command_line_arguments.source
    with shelve.open(path.join(home_dir, '.rss_feed')) as database:
        news_collection = []
        # Search by date and source
        if source:
            for key_date in database:
                if date in key_date:
                    news = database[key_date]
                    if source == news.source:
                        news_collection.append(news)
        # Search only by date
        else:
            for key_date in database:
                if date in key_date:
                    news = database[key_date]
                    news_collection.append(news)
    if news_collection:
        return news_collection
    else:
        if source:
            msg = f"There are no news entries in database on {date} date and {source} source"
            raise ExtractNewsException(msg)
        else:
            msg = f"There are no news entries in database on {date} date"
            raise ExtractNewsException(msg)
