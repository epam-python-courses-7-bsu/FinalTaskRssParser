from dataclasses import dataclass


@dataclass
class Feed:
    """Feed class contains required child elements of channel element from RSS-page"""
    title: str          # <title> title of the channel
    description: str    # <description> describe of the channel
