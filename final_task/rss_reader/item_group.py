import logging
import tools
from dataclasses import dataclass
from typing import List
from item import Item
from parser_rss import format_description
from html import unescape as html_unescape
from colorama import Style, Fore


@dataclass
class ItemGroup:
    feed: str
    items: List[Item]

    def __repr__(self):
        if tools.colorize:
            str_item_group = Style.BRIGHT + Fore.GREEN + 'Feed: ' + Style.NORMAL + Fore.GREEN + self.feed + '\n\n'
        else:
            str_item_group = 'Feed: ' + self.feed + '\n\n'

        for item in self.items:
            str_item_group += str(item) + '\n'

        return str_item_group


def get_item_group_from_feedparser(parser):
    """ Retrieve all items from feedparser and return item group.

    :type parser: 'feedparser.FeedParserDict'

    :rtype: ItemGroup
    """
    items = list()

    logging.info('Loop for retrieving items.')
    for item in parser.entries:
        text, img_links = format_description(item.description)

        if text:
            new_item = Item(
                title=html_unescape(item.title),
                date=item.published,
                link=item.link,
                text=text,
                img_links=img_links
            )

            items.append(new_item)

    return ItemGroup(feed=parser.feed.title, items=items)
