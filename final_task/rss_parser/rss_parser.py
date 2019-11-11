import argparse
import logging
import sys
from os import path, remove

from  final_task.rss_parser.Classes.RSSParser import RSSParser


def create_parser():
    parse = argparse.ArgumentParser()
    parse.add_argument('--version', nargs='?', help='Print version of program', metavar='')
    parse.add_argument('--json', nargs='?', help='Print result as JSON in stdout', metavar='')
    parse.add_argument('--verbose', nargs = '?', help='Outputs verbose status messages', metavar='')
    parse.add_argument('--limit', nargs='?', help='Limit news if this parameter provided', metavar='', type=int,
                       default=None)
    parse.add_argument('source', help='RSS URL')
    return parse


def main(link, limit):
    list_of_args = sys.argv
    if link and (limit is not None):
        logging.info("Started rss_parser with args")
        RSSParser(link, limit, list_of_args)
        logging.info("Finished rss_parser with args")
    elif link:
        print("You have forgotten to input limit!")

    if '--verbose' in list_of_args:
        print()
        with open('mySnake.log') as log:
            for line in log:
                print(line)


if __name__ == '__main__':
    if path.isfile("mySnake.log"):
        remove("mySnake.log")
    logging.basicConfig(filename="mySnake.log", level=logging.INFO)
    logging.info("Program started")
    logging.info("Creating parser for console")
    parser = create_parser()
    logging.info("Created parser for console")
    namespace = parser.parse_args()
    main(namespace.source, namespace.limit)

    # link = "https://news.yahoo.com/rss/"
    # main(link, 5)

    # https://news.yahoo.com/rss/
    # https://www.buzzfeed.com/world.xml
    # https://www.eureporter.co/feed/
    # http://www.politico.eu/feed/
    # https://www.e-ir.info/category/blogs/feed/
    # http://www.globalissues.org/news/feed
    # http://rss.cnn.com/rss/edition_world.rss
    # http://feeds.washingtonpost.com/rss/world -- не работает, мразззз