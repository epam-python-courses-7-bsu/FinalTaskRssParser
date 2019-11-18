""" Module of creation functions and action functions.

    Functions:
    create_logger(com_line_args) -> logger
    get_com_line_args() -> com_line_args
    get_news(command_line_args, logger) -> news_collection
    print_news_stdout(news_collection) -> None
    print_news_json(news_collection) -> None
    print_news(news_collection, com_line_args, logger) -> None """

import feedparser
from bs4 import BeautifulSoup
import html
import argparse
import json
import logging
from rss_reader.models import NewsEntry
from dataclasses import asdict
from rss_reader.validation_functions import check_limit_arg


def create_logger(com_line_args):
    """Create logger function.

       Creates a logger considering the --verbose argument. """
    # Create a logger
    logger = logging.getLogger("rss_reader_logger")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("file.log")

    # Check --verbose argument
    if com_line_args.verbose:
        c_handler.setLevel(logging.DEBUG)
    else:
        c_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    return logger


def get_com_line_args():
    """ Function to get command line arguments. """
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.", add_help=True)
    parser.add_argument("source", type=str, nargs="?", help="RSS URL")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

    return parser.parse_args()


def get_news(command_line_args, logger):
    """ Get news function.

        Uses feedparser library to receive news,
        and BeautifulSoup library to converting news in readable format.  """
    logger.info("Getting news.")
    news_feed = feedparser.parse(command_line_args.source)
    news_collection = {}

    # convert title string to unicode
    feed = {"title": html.unescape(news_feed.feed.get("title", "")),
            "date": news_feed.feed.get("published", ""),
            "language": news_feed.feed.get("language", "")}

    news_collection["feed"] = feed
    news_collection["entries"] = []

    for entry in news_feed.entries:
        news_entry = NewsEntry()
        news_entry.title = html.unescape(entry.get("title", ""))
        news_entry.date = entry.get("published", "")
        news_entry.link = entry.get("link", "")

        # get rid of html tags
        soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
        news_entry.summary = html.unescape(soup.text)

        news_collection["entries"].append(news_entry)

    return news_collection


def print_news_stdout(news_collection):
    """ Function for print news to stdout in text format. """
    print("################################################################################\n",
          "Feed: " + news_collection["feed"]["title"],
          "Publication date: " + news_collection["feed"]["date"],
          "Language: " + news_collection["feed"]["language"] + '\n',
          sep='\n')

    for entry in news_collection["entries"]:
        entry.print_entry()


def print_news_json(news_collection):
    """ Function for print news to stdout in json format. """
    news_collection_for_json = {"feed": news_collection["feed"],
                                "entries": []}

    for entry in news_collection["entries"]:
        entry_for_json = asdict(entry)
        news_collection_for_json["entries"].append(entry_for_json)

    print(json.dumps(news_collection_for_json, indent=4))


def print_news(news_collection, com_line_args, logger):
    """ Function for print news to stdout
        that take account of limit and json arguments. """

    # get valid limit argument
    limit = check_limit_arg(news_collection, com_line_args, logger)
    if len(news_collection["entries"]) < limit:
        logger.warning("The number of news is less than the value of the argument limit.")
        new_news_collection = news_collection
    else:
        new_news_collection = {"feed": news_collection["feed"],
                               "entries": news_collection["entries"][:limit]}

    logger.info("Printing news.")
    if com_line_args.json:
        print_news_json(new_news_collection)
    else:
        print_news_stdout(new_news_collection)
