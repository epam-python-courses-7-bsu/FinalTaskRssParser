import html
from dataclasses import dataclass


@dataclass
class RssItem:
    '''
    Represents a single news from RSS channel
    '''
    title: str
    published: str
    link: str
    media: str

    def __str__(self):
        return f'TITLE: {html.unescape(self.title)}\
            \n\t|| PUBLISHED: {html.unescape(self.published)} \
            \n\t|| LINK: {html.unescape(self.link)}\
            \n\t|| MEDIA: {html.unescape(self.media)}'
