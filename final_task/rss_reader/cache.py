import pickle
import logging
from os import path, makedirs
from dateutil.parser import parse
import time

from exceptions import CacheNotFoundError


# cache storage directory
CACHE_PATH = '/tmp/rss_reader'


def save_cache(news_articles, url):
    """Save news_articles to cache"""
    # cache {date: {url: set(news_articles)}}
    cache = format_cache(news_articles, url)
    for date in cache:
        # cache_from_file {url: set(news_articles)}
        cache_from_file = read_from_file(date)
        result_cache = update_cache(cache_from_file, cache, date, url)
        logging.info(f'Saving cache to {CACHE_PATH}/cache/{date}.cache')
        write_to_file(result_cache, date)
    logging.info('Cache is saved')


def read_cache(date, url, limit):
    # get cache for this url from file
    logging.info(f'Loading cache from {CACHE_PATH}/cache/{date}.cache')
    # cache {url: set(news_articles)}
    cache = read_from_file(date)
    news_articles = []
    if cache:
        if url == 'ALL':
            # get all news for this date
            for outlett in cache:
                for article in cache[outlett]:
                    if len(news_articles) == limit:
                        break
                    news_articles.append(article)
        else:
            # get news only for these url and date
            if cache.get(url):
                list_of_articles = list(cache[url])[:limit]
                for article in list_of_articles:
                    news_articles.append(article)
            else:
                raise CacheNotFoundError
        return news_articles
    else:
        raise CacheNotFoundError


def format_cache(news_articles, url):
    """formatting news_articles to cache format"""
    # cache {date: {url: set(news_articles)}}
    cache = {}
    for article in news_articles:
        # get pubDate from article as as datetime object
        parsed_date = parse(article.pub_date)
        # format date to YYYYmmdd format
        date = parsed_date.strftime('%Y%m%d')

        if date in cache:
            if url in cache[date]:
                cache[date][url].add(article)
            else:
                cache[date][url] = {article}
        else:
            cache[date] = {url: {article}}
    return cache


def update_cache(cache_from_file, cache, date, url):
    if cache_from_file:
        # merge old data from cache with a new one
        # cache {date: {url: set(news_articles)}}
        # result_cache {url: set(news_articles)}
        if url in cache_from_file:
            result_cache = {**cache_from_file, **{url: (cache_from_file[url].union(cache[date][url]))}}
        else:
            result_cache = {**cache_from_file, **{url: cache[date][url]}}
    else:
        # create a new cache if no old one
        result_cache = {url: cache[date][url]}
    return result_cache


def read_from_file(date):
    try:
        with open(f'{CACHE_PATH}/cache/{date}.cache', 'rb') as cache_file:
            cache_from_file = pickle.load(cache_file)
            return cache_from_file
    except Exception as ex:
        logging.info(ex)


def write_to_file(cache, date):
    try:
        if not path.exists(f'{CACHE_PATH}/cache/'):
            makedirs(f'{CACHE_PATH}/cache/')
        with open(f'{CACHE_PATH}/cache/{date}.cache', 'wb') as cache_file:
            pickle.dump(cache, cache_file, protocol=None)
    except Exception as ex:
        logging.info(ex)
