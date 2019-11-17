import argparse
import logging
import sys

import feedparser

from final_task.rss_reader.classes.exceptions import FeedError
from final_task.rss_reader.classes.rss_feed import RssFeed
from final_task.rss_reader.classes.rss_item import RssItem

# common logger init
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s} %(levelname)s - %(message)s'
    )
logger = logging.getLogger('rss_logger')


def init_parser():
    parser = argparse.ArgumentParser(description='RRS feed receiver')
    parser.add_argument('url', help='URL for RSS feed')
    parser.add_argument('--version', help='prints version', action='store_true')
    parser.add_argument('--json', help='converts news to JSON', action='store_true')
    parser.add_argument('--verbose', help='output verbose status messages', action='store_true')
    parser.add_argument('--limit', help='determines the number of showed news.', type=int)

    return parser.parse_args()


def init_news_list(feed_dict, limit):
    news_list = []
    if limit is None or limit > len(feed_dict.entries):
        limit = len(feed_dict.entries)
    for index, entry in enumerate(feed_dict.entries):
        if index == limit:
            break
        title = entry.get('title', 'unknown')
        published = entry.get('published', 'unknown')
        link = entry.get('link', 'no link')
        media_list = entry.get('media_content', 'no media content')
        if isinstance(media_list, list):
            media_link = media_list[0].get('url', 'no media')
            if media_link == '':
                media_link = 'no media'
        news = RssItem(title, published, link, media_link)
        news_list.append(news)
    return news_list


def init_feed(url, limit):
    feed_dict = feedparser.parse(url)
    if feed_dict.bozo:
        raise FeedError('Invalid feed')

    logger.debug('GOT FEED FROM SOURCE')
    logger.debug('FEED INIT')
    news_list = init_news_list(feed_dict, limit)
    feed = RssFeed(feed_dict.feed.title, feed_dict.feed.description, feed_dict.feed.link, news_list)
    logger.debug('DONE')

    return feed


def main():
    args = init_parser()
    logger.disabled = not args.verbose

    if args.version:
        print('version 1.0')
    try:
        news_feed = init_feed(args.url, args.limit)
        if args.json:
            news_feed.toJSON()
        else:
            logger.debug('PRINTING FEED')
            news_feed.print_feed()
    except FeedError as exc:
        print('Error: ' + str(exc))


if __name__ == "__main__":
    main()
