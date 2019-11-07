"""Contain formatting output functions

Functions
---------
check_limit_argument(command_line_args, news_collection, logger) -> news_collection
    Check presence and validness of limit argument
    If present and valid, then limit collection of news
    Uses inside print_feeds() function
--------------------------------------------
generate_news_json(news_collection, logger) -> news_json
    Create json of news
--------------------------------------------
print_feeds(news_collection, command_line_args,logger) -> None
    Print news to stdout in json or text format
"""

import json


def check_limit_argument(command_line_args, news_collection, logger):
    """Check presence and validness of limit argument

    If present and valid, then limit collection of news
    """

    if command_line_args.limit:
        limit = command_line_args.limit
        if len(news_collection) > limit >= 0:
            return news_collection[:limit]
        elif limit < 0:
            logger.warning("Limit argument can't be a negative")
            limit = int(input("Please, enter the valid value: "))
            command_line_args.limit = limit
            return check_limit_argument(command_line_args, news_collection, logger)
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
        if news.links:
            news_dict['links'] = news.links
        all_news_dict['news'].append(news_dict)
    news_json = json.dumps(all_news_dict, indent=4)
    return news_json


def print_feeds(news_collection, command_line_args, logger):
    """Print news to stdout in json or text format"""
    news_collection = check_limit_argument(command_line_args, news_collection, logger)
    if news_collection:
        if command_line_args.json:
            news_json = generate_news_json(news_collection, logger)
            print(news_json)
        else:
            news_collection[0].print_feed_title()
            for news in news_collection:
                news.print_news()
