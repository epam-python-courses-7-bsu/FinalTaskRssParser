from dataclasses import dataclass
from dataclasses import field


@dataclass
class Item:
    """Contains data from articles from RSS-page"""
    title: str          # title of the the info linked in item element
    link: str           # link to the article that described in item element
    image_links: tuple  # link or links to images contained in article
    description: str    # describe of the info linked in item element
    pub_date: str       # Date when article was published

    # Implemented for debugging
    def __str__(self):
        out = str(self.title) + '\n'
        out += str(self.link) + '\n'
        out += str(self.image_links) + '\n'
        out += str(self.description) + '\n'
        out += str(self.pub_date)
        return out
