import argparse
import logging
import items as itms
import parser_rss
import exceptions
import news_converter
from log import turn_on_logging
from news_storage import save_news, get_news_by_date
from datetime import datetime


STORAGE_FILE = 'news.data'
VERSION = '3.0'


def create_arg_parser():
    """ Create and return argument parser.

    :return: argument parser
    :rtype: 'argparse.ArgumentParser'
    """
    arg_parser_ = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')

    arg_parser_.add_argument('--source', type=str, help='RSS URL')
    arg_parser_.add_argument('--version', action='version', help='Print version info', version='%(prog)s v' + VERSION)
    arg_parser_.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    arg_parser_.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    arg_parser_.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')
    arg_parser_.add_argument('--date', type=lambda d: datetime.strptime(d, '%Y%m%d'),
                             help='News from the specified day will be printed out. Format: YYYYMMDD')

    return arg_parser_


def print_news(json_arg, item_group):
    """ Print news in stdout

    :param json_arg: if True news print as json
    :type json_arg: bool
    :type item_group: 'items.ItemGroup'
    """
    if json_arg:
        logging.info('Converting item group to json string.')
        json_str = news_converter.news_as_json_str(item_group)

        logging.info('Printing news as json.')
        print(json_str)
    else:
        logging.info('Printing news.')
        itms.print_item_group(item_group)


def print_news_from_list(json_arg, news):
    """ Print news in stdout

    :param json_arg: if True news print as json
    :type json_arg: bool
    :type news: list of 'items.ItemGroup'
    """
    if json_arg:
        logging.info('Converting list of item group to json string.')
        json_str = news_converter.news_as_json_str_from_list(news)

        logging.info('Printing news as json.')
        print(json_str)
    else:
        for news_group in news:
            print_news(json_arg, news_group)
            print('\n-------------------------------------------------------------------------------------\n')


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    if args.verbose:
        logging.info('Turning on logging.')
        turn_on_logging(logging.getLogger())

    if not args.source and not args.date:
        logging.error('Source or/and date must be specified.')
        arg_parser.print_help()
    elif not args.limit or args.limit > 0:
        main_working(args)
    else:
        logging.error('Incorrect limit value!')


def main_working(args):
    if args.date:
        try:
            logging.info('Getting news by date ' + str(args.date) + ' from storage ' + STORAGE_FILE)
            news_by_date = get_news_by_date(args.date, STORAGE_FILE, args.source, args.limit)
        except exceptions.StorageNotFoundError as exc:
            logging.error(exc)
        except exceptions.NewsNotFoundError as err:
            logging.error(err)
        else:
            print_news_from_list(args.json, news_by_date)
    else:
        try:
            logging.info('Creating feedparser.')
            rss_feedparser = parser_rss.create_feedparser(args.source, args.limit)

            logging.info('Getting items.')
            item_group = itms.get_item_group_from_feedparser(rss_feedparser)

        except ValueError as err:
            logging.error(err)
        except exceptions.GettingRSSException as exc:
            logging.error(exc)
        except TypeError as err:
            logging.error(err)
        else:
            logging.info('Saving news in ' + STORAGE_FILE)
            save_news(args.source, item_group, STORAGE_FILE)

            print_news(args.json, item_group)


if __name__ == '__main__':
    main()
