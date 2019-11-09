from dataclasses import dataclass


@dataclass
class Item:
    """Item class contains required child elements of item element from RSS-page"""
    title: str          # <title> title of the channel
    link: str           # <link> link to the article that described in item element
    description: str    # <description> describe of the channel
