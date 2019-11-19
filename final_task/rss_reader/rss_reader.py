import argparse
import logging
import sys

import feedparser
from tinydb import TinyDB, where

from rss_feed import RssFeed
from rss_item import RssItem
from exceptions_ import FeedError

# common logger init
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s} %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger('rss_logger')


def init_parser():
    parser = argparse.ArgumentParser(description='RRS feed receiver')
    parser.add_argument('url', help='URL for RSS feed', nargs='?')
    parser.add_argument('--version', help='prints version', action='store_true')
    parser.add_argument('--json', help='converts news to JSON', action='store_true')
    parser.add_argument('--verbose', help='output verbose status messages', action='store_true')
    parser.add_argument('--limit', help='determines the number of showed news.', type=int)
    parser.add_argument('--date', help='shows cached news at given date', type=str, default=None)

    return parser.parse_args()


def init_news_list(feed_dict, limit, url):
    news_list = []
    if limit is None or limit > len(feed_dict.entries) or limit < 0:
        limit = len(feed_dict.entries)
    entries = feed_dict.entries[:limit]

    for _, entry in enumerate(entries):
        title = entry.get('title', 'unknown')
        published = entry.get('published', 'unknown')
        published_parsed = entry.get('published_parsed', 'unknown')
        published_parsed_string = str(published_parsed[0]) + \
            str(published_parsed[1]) + str(published_parsed[2])
        link = entry.get('link', 'no link')
        media_list = entry.get('media_content', 'no media content')
        media_link = 'no media content'
        if isinstance(media_list, list):
            media_link = media_list[0].get('url', 'no media')
            if media_link == '':
                media_link = 'no media'
        news = RssItem(title, published, link, media_link, url, published_parsed_string)
        news_list.append(news)
    return news_list


def init_feed(url, limit):
    feed_dict = feedparser.parse(url)
    if feed_dict.bozo:
        raise FeedError('Invalid feed')

    LOGGER.debug('GOT FEED FROM SOURCE')
    LOGGER.debug('FEED INIT')
    news_list = init_news_list(feed_dict, limit, url)
    feed = RssFeed(feed_dict.feed.title, feed_dict.feed.description, feed_dict.feed.link, news_list)
    LOGGER.debug('DONE')

    return feed


def get_news_by_date(source, date, limit):
    '''
    Gives news by date and source if specified

    database.search returns Mapping object which used for
    news_item initialization
    '''
    LOGGER.debug('READING DATABASE')
    database = TinyDB('db.json')
    LOGGER.debug('CHECKING INPUT')
    if source:
        LOGGER.debug('DATE AND SOURCE ARE SPECIFIED')
        news_list = database.search((where('date') == date) & (where('source') == source))
    else:
        LOGGER.debug('ONLY DATE IS SPECIFIED')
        news_list = database.search((where('date') == date))
    LOGGER.debug('PRINTING...')
    if len(news_list) == 0:
        print("No news found")
    if limit is None or limit > len(news_list) or limit < 0:
        limit = len(news_list)
    news_list = news_list[:limit]
    for _, news_dict in enumerate(news_list):
        news_item = RssItem.from_dict(news_dict)
        print(news_item)


def main():
    args = init_parser()
    LOGGER.disabled = not args.verbose

    if args.version:
        print('version 1.3')
    try:
        if args.date and args.url:
            get_news_by_date(args.url, args.date, args.limit)
        elif args.url:
            news_feed = init_feed(args.url, args.limit)
            if args.json:
                news_feed.to_json()
                news_feed.cache('db.json')
            else:
                LOGGER.debug('PRINTING FEED')
                news_feed.print_feed()
                news_feed.cache('db.json')
        elif args.date:
            get_news_by_date(None, args.date, args.limit)
        else:
            print('Positional argument \'url\' is required')
            sys.exit(1)

    except FeedError as exc:
        print('Error: ' + str(exc))


if __name__ == "__main__":
    main()
