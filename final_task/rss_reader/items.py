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


@dataclass
class ItemGroup:
    feed: str
    items: List[Item]


def print_item_group(item_group):
    """ Print item group in stdout.

    :type item_group: ItemGroup
    """
    print('Feed: ' + item_group.feed)

    for item in item_group.items:
        print(f'\nTitle: {item.title}'
              f'\nDate: {item.date}'
              f'\nLink: {item.link}'
              f'\nText: {item.text}')

        if item.img_links:
            print('Image links: ')
            for num, link in enumerate(item.img_links):
                print(f'\t[{num + 1}]: [{link}]')


def get_item_group_from_feedparser(parser):
    """ Retrieve all items from feedparser and return item group.

    :type parser: 'feedparser.FeedParserDict'

    :raise TypeError: if type of parser is not 'feedparser.FeedParserDict'

=    :rtype: ItemGroup
    """

    if not isinstance(parser, FeedParserDict):
        raise TypeError(f'Wrong type: {type(parser)}. Expected type of parser: {FeedParserDict}')

    items = list()

    logging.info('Loop for retrieving items.')
    for item in parser.entries:
        text, img_links = format_description(item.description)

        new_item = Item(
            title=html_unescape(item.title),
            date=item.published,
            link=item.link,
            text=text,
            img_links=img_links
        )

        items.append(new_item)

    return ItemGroup(feed=parser.feed.title, items=items)
