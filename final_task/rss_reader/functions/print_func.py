"""Contain formatting output functions"""

import json
import classes.exceptions as exc


def check_limit_argument(command_line_args, news_collection, logger):
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
    all_news_dict = {
                    'Feed': news_collection[0].feed_title,
                    'news': []
                    }
    logger.info("Configure json file...")
    for news in news_collection:
        news_dict = {}
        news_dict['title'] = news.title
        news_dict['date'] = news.date
        news_dict['link'] = news.link
        news_dict['text'] = news.text

        news.create_string_of_links()
        if news.links:
            list_of_links = news.links.split('\n')
            news_dict['links'] = list_of_links
        all_news_dict['news'].append(news_dict)
    news_json = json.dumps(all_news_dict, indent=4, ensure_ascii=False)
    return news_json


def print_feeds(news_collection, command_line_args, logger):
    """Print news to stdout in json or text format"""
    news_collection = check_limit_argument(command_line_args, news_collection, logger)
    if news_collection:
        if command_line_args.json:
            news_json = generate_news_json(news_collection, logger)
            logger.info("Json successful configured")
            logger.info("Printing json:")
            print(news_json)
        else:
            logger.info("Printing news:")
            news_collection[0].print_feed_title()
            for num, news in enumerate(news_collection):
                logger.info("Printing news №{}:".format(num+1))
                news.print_news()


def generate_news_json_from_database(news_collection, logger):
    """Create json of news"""
    all_news_dict = {'news': []}
    logger.info("Configure json file...")
    for news in news_collection:
        news_dict = {}
        news_dict['Feed'] = news.feed_title,
        news_dict['title'] = news.title
        news_dict['date'] = news.date
        news_dict['link'] = news.link
        news_dict['text'] = news.text

        news.create_string_of_links()
        if news.links:
            list_of_links = news.links.split('\n')
            news_dict['links'] = list_of_links
        all_news_dict['news'].append(news_dict)
    news_json = json.dumps(all_news_dict, indent=4, ensure_ascii=False)
    return news_json


def print_feeds_from_database(news_collection, command_line_args, logger):
    """Print news to stdout in json or text format"""
    news_collection = check_limit_argument(command_line_args, news_collection, logger)
    if news_collection:
        if command_line_args.json:
            news_json = generate_news_json_from_database(news_collection, logger)
            logger.info("Json successful configured")
            logger.info("Printing json:")
            print(news_json)
        else:
            logger.info("Printing news:")
            for num, news in enumerate(news_collection):
                logger.info("Printing news №{}:".format(num+1))
                news.print_feed_title()
                news.print_news()
