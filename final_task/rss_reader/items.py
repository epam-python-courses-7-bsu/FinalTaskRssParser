import logging
from dataclasses import dataclass
from typing import List
from feedparser import FeedParserDict
from parser_rss import format_description
from html import unescape as html_unescape


@dataclass
class Item:
    title: str
    date: str
    link: str
    text: str
    img_links: List[str]


def print_items(items):
    """ Print all items in stdout.

    :param items: just all items
    :type items: list of Item
    """
    for item in items:
        print(f'\nTitle: {item.title}'
              f'\nDate: {item.date}'
              f'\nLink: {item.link}'
              f'\nText: {item.text}')

        if item.img_links:
            print('Image links: ')
            for num, link in enumerate(item.img_links):
                print(f'\t[{num + 1}]: [{link}]')


def get_items_from_feedparser(parser):
    """ Retrieve all items from feedparser and convert them to Item.

    :param parser: feedparser
    :type parser: 'feedparser.FeedParserDict'

    :raise TypeError: if type of parser is not 'feedparser.FeedParserDict'

    :return: items
    :rtype: list if Item
    """

    if not isinstance(parser, FeedParserDict):
        raise TypeError(f'Wrong type: {type(parser)}. Expected type of parser: {FeedParserDict}')

    items = list()

    logging.info('Loop for creating items.')
    for item in parser.entries:
        text_, img_links_ = format_description(item.description)

        new_item = Item(
            title=html_unescape(item.title),
            date=item.published,
            link=item.link,
            text=text_,
            img_links=img_links_
        )

        items.append(new_item)

    return items
