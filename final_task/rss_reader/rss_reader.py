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
            if not check.internet_connection_check():
                raise ex.NoInternetConnection("No internet connection")
            parsed = feedparser.parse(rss)
            if parsed.bozo > 0:
                raise ex.InvalidURLAddress("Invalid RSS URL address")
            logging.info('parsed url: %s', rss)
        else:
            parsed = {}
        feed_obj = feed.Feed(parsed, args)

        if not args.date:
            feed_obj.save_feed_to_database()

<<<<<<< HEAD
        to_print = True

        if args.to_html:
            feed_obj.save_feed_to_html()
            to_print = False
        if args.to_pdf:
            feed_obj.save_feed_to_pdf()
            to_print = False
            
        if to_print:
            if args.json:
                feed_obj.print_json_feed(args.colorize)
            else:
                feed_obj.print_readable_feed(args.colorize)

=======
        if args.json:
            feed_obj.print_json_feed()
        elif args.to_html:
            feed_obj.save_feed_to_html()
        elif args.to_pdf:
            feed_obj.save_feed_to_pdf()
        else:
            feed_obj.print_readable_feed()
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
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
