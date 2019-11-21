from os import path
import datetime
import pickle
import logging


def format_cache(news_articles, url):
    """formatting news_articles to cache format"""
    cache = {}
    for article in news_articles:
        # get pubDate from article as as datetime object
        print(article.pub_date)
        pub_date = ' '.join(article.pub_date.split(' ')[1:4])
        parsed_date = datetime.datetime.strptime(pub_date, '%d %b %Y')
        # format date to YYYYmmdd format
        date = parsed_date.strftime('%Y%m%d')

        # create cache with a structure like
        # {date1: {url: set(article1, article2, ...)}, ...}
        if date in cache:
            if url in cache[date]:
                cache[date][url].add(article)
            else:
                cache[date][url] = {article}
        else:
            cache[date] = {url: {article}}
    return cache


def update_cache(news_articles, url):
    """Save news_articles to cache"""
    logging.info('Updating cache')
    cache = format_cache(news_articles, url)
    for date in cache:
        cache_from_file = read_from_file(date)
        # if exist: update cache file
        # or create a new one if it doesn't
        if cache_from_file:
            # merge old data from cache with a new one
            if url in cache_from_file:
                result_cache = {**cache_from_file, **{url: (cache_from_file[url].union(cache[date][url]))}}
            else:
                result_cache = {**cache_from_file, **{url: cache[date][url]}}
        else:
            result_cache = {url: cache[date][url]}
        write_to_file(result_cache, date)
    logging.info('Cache is updated')


def read_cache(date, url):
    # get cache for this url from file
    cache = read_from_file(date)
    if cache:
        if url == 'ALL':
            # get all news for this date
            for outlett in cache:
                for article in cache[outlett]:
                    yield article
        else:
            # get news only for these url and date
            if cache.get(url):
                for article in cache[url]:
                    yield article
            else:
                print(F'Cache for {url} or {date} do not exist')

    else:
        print(F'Cache for {url} or {date} do not exist')


def read_from_file(date):
    try:
        if path.exists(f'{date}.cache'):
            with open(f'{date}.cache', 'rb') as cache_file:
                cache_from_file = pickle.load(cache_file)
                return cache_from_file
    except Exception as ex:
        logging.info(ex)


def write_to_file(cache, date):
    try:
        with open(f'{date}.cache', 'wb') as cache_file:
            pickle.dump(cache, cache_file, protocol=None)
    except Exception as ex:
        logging.info(ex)
