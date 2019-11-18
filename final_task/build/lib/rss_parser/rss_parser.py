import argparse
import logging
import sys
from os import path, remove

from Classes.RSSParser import RSSParser


def create_parser():
    parse = argparse.ArgumentParser()
    parse.add_argument('--version', nargs='?', help='Print version of program', metavar='')
    parse.add_argument('--json', nargs='?', help='Print result as JSON in stdout', metavar='')
    parse.add_argument('--verbose', nargs='?', help='Outputs verbose status messages', metavar='')
    parse.add_argument('--date', nargs='?', help='Read news from this date', metavar='',
                       default=None)
    parse.add_argument('--limit', nargs='?', help='Limit news if this parameter provided', metavar='', type=int,
                       default=None)
    parse.add_argument('source', help='RSS URL')
    return parse


def main(link, limit, list_of_arguments):
    if link and (limit is not None) and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif '--version' in list_of_arguments and (limit is not None):
        print("\nVERSION: 1.0")
        RSSParser(link, limit, list_of_arguments).parse()
    elif link and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif link and (limit is not None):
        logging.info("Started rss_parser with args")
        RSSParser(link, limit, list_of_arguments).parse()
        logging.info("Finished rss_parser with args")
    elif '-version' in list_of_arguments:
        print("\nVERSION: 1.0")
    elif link:
        RSSParser(link, limit, list_of_arguments).parse()

    if '--verbose' in list_of_arguments:
        print()
        with open('Snake.log') as log:
            for line in log:
                print(line)


if __name__ == '__main__':
    list_of_args = tuple(sys.argv)
    if path.isfile("Snake.log"):
        remove("Snake.log")
    logging.basicConfig(filename="Snake.log", level=logging.INFO)
    logging.info("Program started")
    logging.info("Creating parser for console")
    parser = create_parser()
    logging.info("Created parser for console")
    namespace = parser.parse_args()
    main(namespace.source, namespace.limit, list_of_args)
