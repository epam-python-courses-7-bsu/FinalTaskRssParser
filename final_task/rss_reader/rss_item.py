import html
import json
from dataclasses import dataclass


@dataclass
class RssItem:
    '''
    Represents a single news from RSS channel

    source: stores link to rss channel of the news
    date: stores date on YYYY%MM%DD format
    '''
    title: str
    published: str
    link: str
    media: str
    source: str
    date: str

    @classmethod
    def from_dict(cls, item_dict) -> 'RssItem':
        return cls(
            title=item_dict['title'],
            published=item_dict['published'],
            link=item_dict['link'],
            media=item_dict['media'],
            source=item_dict['source'],
            date=item_dict['date']
            )

    def __str__(self):
        return f'TITLE: {html.unescape(self.title)}\
            \n\t|| PUBLISHED: {html.unescape(self.published)} \
            \n\t|| LINK: {html.unescape(self.link)}\
            \n\t|| MEDIA: {html.unescape(self.media)}'
