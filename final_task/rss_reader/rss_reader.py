import argparse
import logging
import sys
from os import path, remove
from Classes.rss_read import RSSParser


def create_parser():
    parse = argparse.ArgumentParser()
    parse.add_argument('--version', nargs='?', help='Print version of program', metavar='')
    parse.add_argument('--json', nargs='?', help='Print result as JSON in stdout', metavar='')
    parse.add_argument('--verbose', nargs='?', help='Outputs verbose status messages', metavar='')
    parse.add_argument('--date', help='Read news from this date', metavar='', default=None)
    parse.add_argument('--limit', nargs='?', help='Limit news if this parameter provided', metavar='', type=int,
                       default=None)
    parse.add_argument('--to-pdf', help='Transfer news to PDF file. It should receive path', metavar='')
    parse.add_argument('--to-html', help='Transfer news to html file. It should receive path', metavar='')
    parse.add_argument('source', nargs='?', help='RSS URL', default=None)
    return parse


def main(link, limit, list_of_arguments):

    if link and (limit is not None) and '--to-html' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).parse()
    elif link and (limit is not None) and '--to-pdf' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).parse()
    elif link and (limit is not None) and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).parse()
    elif link != '' and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).parse()
    elif link != '' and '--to-pdf' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).parse()
    elif link and (limit is not None):
        logging.info("Started rss_reader with args")
        RSSParser(link, limit, list_of_arguments).parse()
        logging.info("Finished rss_reader with args")
    elif limit is not None and '--date' in list_of_arguments:
        RSSParser(link, limit, list_of_arguments).news_for_date()
    elif link:
        print("A")
        RSSParser(link, limit, list_of_arguments).parse()


if __name__ == '__main__':
    list_of_args = tuple(sys.argv)
    if '--version' in list_of_args:
        print("VERSION 1.0")
    if path.isfile("snake.log"):
        remove("snake.log")
    logging.basicConfig(filename="snake.log", level=logging.INFO)
    logging.info("Program started")
    logging.info("Creating parser for console")
    parser = create_parser()
    logging.info("Created parser for console")
    namespace = parser.parse_args()
    main(namespace.source, namespace.limit, list_of_args)
