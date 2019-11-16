import feed
import feedparser
import ssl
import logging
from args_creater import arguments


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def main():
    """main function"""
    args = arguments()

    rss = args.source

    logging_level = 'WARNING'
    if args.verbose:
        logging_level = 'INFO'

    logging.basicConfig(level=logging_level,)
    logging.info('Started')

    parsed = feedparser.parse(rss)
    if 'bozo_exception' in parsed.keys():
        print('invalid url')
        exit()
    logging.info('parsed url: %s', rss)

    feed_size = len(parsed.entries)
    if args.limit:
        if args.limit > feed_size:
            print("Only %s articles is avaliable", feed_size)
            number_of_articles = feed_size
        else:
            number_of_articles = args.limit
    else:
        number_of_articles = feed_size

    my_feed = feed.Feed(parsed, number_of_articles)

    if args.json:
        my_feed.print_json_feed()
    else:
        my_feed.print_readable_feed()

    logging.info('Finished')


if __name__ == "__main__":
    main()
