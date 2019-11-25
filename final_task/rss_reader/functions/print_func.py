"""Contain formatting output functions"""

import json
from termcolor import cprint
from dataclasses import asdict

import classes.exceptions as exc


def limit_news_collections(command_line_args, news_collection, logger):
    """Check presence and validness of limit argument

    If present and valid, then limit collection of news
    """
    if command_line_args.limit or command_line_args.limit == 0:
        limit = command_line_args.limit
        if limit < 0:
            raise exc.LimitArgumentError("Limit argument can't be negative!")
        elif len(news_collection) > limit >= 0:
            return news_collection[:limit]
        else:
            logger.warning("Limit argument is longer then list of avaliable news")
            return news_collection
    else:
        return news_collection


def generate_news_json(news_collection, logger):
    """Create json of news"""
    all_news_dict = {'news': []}
    logger.info("Configure json file...")
    for news in news_collection:
        news_dict = asdict(news)
        links = news.create_string_of_links()
        if links:
            list_of_str_links = links.split('\n')
            news_dict['links'] = list_of_str_links
        all_news_dict['news'].append(news_dict)
    news_json = json.dumps(all_news_dict, indent=4, ensure_ascii=False)
    return news_json


def print_feeds(news_collection, command_line_args, logger):
    """Print news to stdout in json or text format"""
    news_collection = limit_news_collections(command_line_args, news_collection, logger)
    if news_collection:
        if command_line_args.json:
            news_json = generate_news_json(news_collection, logger)
            logger.info("Json successful configured")
            logger.info("Printing json:")
            col_print(news_json, command_line_args, 'cyan')
        else:
            logger.info("Printing news:")
            news_collection[0].print_feed_title()
            for num, news in enumerate(news_collection):
                logger.info("Printing news №{}:".format(num+1))
                news.print_news()


def print_feeds_from_database(news_collection, command_line_args, logger):
    """Print news to stdout in json or text format"""
    news_collection = limit_news_collections(command_line_args, news_collection, logger)
    if news_collection:
        if command_line_args.json:
            news_json = generate_news_json(news_collection, logger)
            logger.info("Json successful configured")
            logger.info("Printing json:")
            col_print(news_json, command_line_args, 'cyan')
        else:
            logger.info("Printing news:")
            for num, news in enumerate(news_collection):
                logger.info("Printing news №{}:".format(num+1))
                news.print_feed_title()
                news.print_news()


def col_print(text, command_line_arguments, color):
    """If colorize argument, prints in color"""
    if command_line_arguments.colorize:
        cprint(text, color)
    else:
        print(text)
