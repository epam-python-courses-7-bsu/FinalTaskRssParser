import argparse
import base64
import html
import logging
import os, sys

import feedparser
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, where

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from converters import to_html, to_pdf
from exceptions_ import FeedError, InvalidArgs, ConvertionError
from rss_feed import RssFeed
from rss_item import RssItem

# common logger init
LOGGER = logging.getLogger('rss_logger')


def init_parser():
    # I really dunno how to test this
    parser = argparse.ArgumentParser(description='RRS feed receiver')
    parser.add_argument('source', help='URL for RSS feed', nargs='?')
    parser.add_argument('--version', help='prints version', action='store_true')
    parser.add_argument('--json', help='converts news to JSON', action='store_true')
    parser.add_argument('--verbose', help='output verbose status messages', action='store_true')
    parser.add_argument('--limit', help='determines the number of showed news.', type=int)
    parser.add_argument('--date', help='shows cached news at given date', type=str, default=None)
    parser.add_argument('--to_pdf', help='coverts news to PDF.', type=str, default=None)
    parser.add_argument('--to_html', help='coverts news to HTML.', type=str, default=None)

    return parser.parse_args()


def get_img_base64(url):
    LOGGER.debug('GETTING IMAGE')
    try:
        img_info = requests.get(url)
        return str(base64.b64encode(img_info.content))
    except Exception:
        return 'no image'


def extract_text_from_html(html_str):
    html_str = html.unescape(html_str)
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.text


def init_news_dict(entry):
    '''
    Initializes single news item from given entry from feedparser
    entry: dict
    Does not init source field
    '''
    title = entry.get('title', 'unknown')
    description = entry.get('description', 'unknown')
    description = extract_text_from_html(description)
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
    base64img = None
    if media_link[:4] == 'http':
        base64img = get_img_base64(media_link)

    item_dict = {
        "title": title,
        "published": published,
        "description": description,
        "link": link,
        "media": media_link,
        "date": published_parsed_string,
        "img": base64img
    }
    return item_dict


def init_news_list(feed_dict, limit, url):
    '''
    Inits news list

    returns RssItem list
    '''
    news_list = []
    if limit is None or limit > len(feed_dict.entries) or limit < 0:
        limit = len(feed_dict.entries)
    entries = feed_dict.entries[:limit]

    for _, entry in enumerate(entries):
        news_dict = init_news_dict(entry)
        news_dict['source'] = url
        news = RssItem.from_dict(news_dict)
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


def print_news_by_date(news_list, args):
    LOGGER.debug('PRINTING...')
    if args.json:
        for _, news_dict in enumerate(news_list):
            news_item = RssItem.from_dict(news_dict)
            news_item.to_json()
    else:
        for _, news_dict in enumerate(news_list):
            news_item = RssItem.from_dict(news_dict)
            print(news_item)


def get_news_by_date(args):
    '''
    Gives news by date and source if specified

    database.search returns Mapping object which used for
    news_item initialization

    Raises FeedError exception if there are no news found
    '''
    LOGGER.debug('READING DATABASE')
    database = TinyDB('db.json')
    LOGGER.debug('CHECKING INPUT')

    if args.source:
        LOGGER.debug('DATE AND SOURCE ARE SPECIFIED')
        news_list = database.search((where('date') == args.date) & (where('source') == args.source))
    else:
        LOGGER.debug('ONLY DATE IS SPECIFIED')
        news_list = database.search((where('date') == args.date))
    database.close()
    if len(news_list) == 0:
        raise FeedError('No news found')
    limit = args.limit
    if args.limit is None or args.limit > len(news_list) or args.limit < 0:
        limit = len(news_list)
    news_list = news_list[:limit]

    if args.to_html:
        to_html(args.to_html, news_list)
        return
    if args.to_pdf:
        to_pdf(args.to_pdf, news_list)
        return
    print_news_by_date(news_list, args)


def main():
    args = init_parser()
    if args.verbose:
        logging.basicConfig(
            format='[%(asctime)s] {%(filename)s} %(levelname)s - %(message)s'
            )
        LOGGER.setLevel('DEBUG')

    try:
        if args.version:
            print('version 1.4')
        # if get news from cache
        elif args.date:
            get_news_by_date(args)
        # if get news from the source
        elif args.source:
            news_feed = init_feed(args.source, args.limit)

            if args.to_html:
                to_html(args.to_html, news_feed.get_news_as_dicts(args.limit))
            elif args.to_pdf:
                to_pdf(args.to_pdf, news_feed.get_news_as_dicts(args.limit))
            # print as json
            elif args.json:
                news_feed.to_json()
                news_feed.cache('db.json')
            # print as usual
            else:
                LOGGER.debug('PRINTING FEED')
                news_feed.print_feed()
                news_feed.cache('db.json')
        else:
            raise InvalidArgs('Positional argument "source" is required')
    except FeedError as exc:
        print('Error: ' + str(exc))


if __name__ == "__main__":
    main()
