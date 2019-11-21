from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    title: str
    date: str
    link: str
    text: str
    img_links: List[str]

    def __repr__(self):
        str_item = f'Title: {self.title}' + \
                   f'\nDate: {self.date}' + \
                   f'\nLink: {self.link}' + \
                   f'\nText: {self.text}\n'

        if self.img_links:
            str_item += 'Image links:\n'
            for num, link in enumerate(self.img_links):
                str_item += f'\t[{num + 1}]: [{link}]\n'

        return str_item
