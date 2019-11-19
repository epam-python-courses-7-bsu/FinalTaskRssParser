import feed
import feedparser
import ssl
import logging
import exceptions as ex
import check_func as check
from args_creater import arguments

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def main():
    """main function"""
    try:
        args = arguments()
        rss = args.source

        logging_level = 'WARNING'
        if args.verbose:
            logging_level = 'INFO'
        logging.basicConfig(level=logging_level,)
        logging.info('Started')

        if not args.date:
            check.internet_connection_check()
            parsed = feedparser.parse(rss)
            if parsed.bozo > 0:
                raise ex.InvalidURLAddress("Invalid RSS URL address")
            logging.info('parsed url: %s', rss)
        else:
            parsed = {}
        feed_obj = feed.Feed(parsed, args)
        if not args.date:
            feed_obj.save_feed_to_database()

        if args.json:
            feed_obj.print_json_feed()
        else:
            feed_obj.print_readable_feed()
    except (
        ex.InvalidURLAddress,
        ex.NoInternetConnection,
        ex.EmptyDataBase,
        ex.DateNotInDatabase
    ) as E:
        print(E)


if __name__ == "__main__":
    main()
    logging.info('Finished')
