"""Module contain definition of "News" class"""

from dataclasses import dataclass

@dataclass
class News:
    """Class that represent single entry of news

    Uses for storing title, date, link, text and links from text
    as an attributes of class.
    """
    title: str
    date: str
    link: str
    text: str
    links: str


    def print_feed_title(self):
        """Print feed title"""
        print(self.feed_title)


    def print_news(self):
        """Print to stdout title, date, link, text
        and links from text in particular sequence."""
        print('-----------------------------------------------------------')
        print('Title: '+self.title)
        print('Date: '+self.date)
        print('Link: '+self.link)
        print()
        print(self.text)
        print()
        if self.links:
            print('Links:')
            print(self.links)
        print('-----------------------------------------------------------')
