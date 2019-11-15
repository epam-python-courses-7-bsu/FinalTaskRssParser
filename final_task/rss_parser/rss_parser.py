import argparse
import logging
import sys
from os import path, remove
from Classes.RSSParser import RSSParser
import re
from Output_functions import verbose


def create_parser():
    parse = argparse.ArgumentParser()
    parse.add_argument('--version', nargs='?', help='Print version of program', metavar='')
    parse.add_argument('--json', nargs='?', help='Print result as JSON in stdout', metavar='')
    parse.add_argument('--verbose', nargs='?', help='Outputs verbose status messages', metavar='')
    parse.add_argument('--date', help='Read news from this date', metavar='', default=None)
    parse.add_argument('--limit', nargs='?', help='Limit news if this parameter provided', metavar='', type=int,
                       default=None)
    parse.add_argument('--source', nargs='?', help='RSS URL', metavar='', default=None)
    # parse.add_argument('source', help='RSS URL', default=None)
    return parse


def main(link, limit, list_of_arguments):

    if link and (limit is not None) and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif link and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif link and (limit is not None):
        logging.info("Started rss_parser with args")
        RSSParser(link, limit, list_of_arguments).parse()
        logging.info("Finished rss_parser with args")
    elif limit is not None and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif link:
        RSSParser(link, limit, list_of_arguments).parse()


if __name__ == '__main__':
    list_of_args = tuple(sys.argv)
    print(list_of_args)
    if '--version' in list_of_args:
        print("VERSION 1.0")
    if path.isfile("Snake.log"):
        remove("Snake.log")
    logging.basicConfig(filename="Snake.log", level=logging.INFO)
    logging.info("Program started")
    logging.info("Creating parser for console")
    parser = create_parser()
    logging.info("Created parser for console")
    namespace = parser.parse_args()
    main(namespace.source, namespace.limit, list_of_args)
