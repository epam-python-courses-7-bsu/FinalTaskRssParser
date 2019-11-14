import argparse
import logging
import items as itms
import parser_rss
from log import turn_on_logging
from news_converter import news_as_json_str


def create_arg_parser():
    """ Create and return argument parser.

    :return: argument parser
    :rtype: 'argparse.ArgumentParser'
    """
    arg_parser_ = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')

    arg_parser_.add_argument('source', type=str, help='RSS URL')
    arg_parser_.add_argument('--version', action='version', help='Print version info', version='%(prog)s v2.0')
    arg_parser_.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    arg_parser_.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    arg_parser_.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')

    return arg_parser_


def print_news(json_arg, rss_parser_, items_):
    """ Print news in stdout """
    if json_arg:
        logging.info('Printing news as json.')
        print(news_as_json_str(rss_parser_.feed.title, items_))
    else:
        logging.info('Printing news.')
        print(f'Feed: {rss_parser_.feed.title}')
        itms.print_items(items_)


def main_working():
    if not args.limit or args.limit > 0:
        try:
            logging.info('Creating feedparser.')
            rss_pars = parser_rss.create_feedparser(args.source, args.limit)

            logging.info('Getting items.')
            items = itms.get_items_from_feedparser(rss_pars)

        except parser_rss.GettingRSSException as exc:
            logging.error(exc)
        except TypeError as exc:
            logging.error(exc)
        else:
            print_news(args.json, rss_pars, items)

    else:
        logging.error('Incorrect limit value!')


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    if args.verbose:
        turn_on_logging(logging.getLogger())

    main_working()
