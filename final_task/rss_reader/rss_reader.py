import argparse
import feedparser
from classes.rss_item import rss_item
from classes.rss_feed import rss_feed
from classes.exceptions import FeedError
from classes.logger import logger


def init_parser():
    parser = argparse.ArgumentParser(description='RRS feed receiver')
    parser.add_argument('url', help='URL for RSS feed')
    parser.add_argument('--version', help='prints version', action='store_true')
    parser.add_argument('--json', help='converts news to JSON', action='store_true')
    parser.add_argument('--verbose', help='output verbose status messages', action='store_true')
    parser.add_argument('--limit', help='determines the number of showed news. Default is 3', type=int, default=3)

    return parser.parse_args()

def init_feed(url, limit):
    feed_dict = feedparser.parse(url)
    if len(feed_dict.entries) == 0:
        raise FeedError('Invalid feed')

    if len(feed_dict.entries) < limit:
        raise FeedError('Not enough news in feed')

    logger.log('GOT FEED FROM SOURCE')
    logger.log('FEED INIT')

    news_list = []
    for index in range(0, limit):
        tit = feed_dict.entries[index].get('title', 'unknown')
        pub = feed_dict.entries[index].get('published', 'unknown')
        lnk = feed_dict.entries[index].get('link', 'no link')
        med = feed_dict.entries[index].get('media_content', 'no media content')
        if isinstance(med, list):
            med = med[0].get('url', 'no media')
        news = rss_item(tit, pub, lnk, med)
        news_list.append(news)
    
    feed = rss_feed(feed_dict.feed.title, feed_dict.feed.description, feed_dict.feed.link, news_list)
    logger.log('DONE')

    return feed

def main():
    args = init_parser()
    logger.is_log_on = args.verbose
    if args.version:
        print('version 1.0')

    try:
        news_feed = init_feed(args.url, args.limit)
        if args.json:

            news_feed.toJSON()

        else:

            logger.log('PRINTING FEED')

            news_feed.print_feed()
    except FeedError as exc:
        print('Error: ' + str(exc))

if __name__ == "__main__":
    main()
