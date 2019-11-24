from dataclasses import dataclass
from typing import List
from colorama import init as init_color, Fore, Style
import tools


@dataclass
class Item:
    title: str
    date: str
    link: str
    text: str
    img_links: List[str]

    def __repr__(self):
        if tools.colorize:
            init_color()
            str_item = f'{Style.BRIGHT + Fore.LIGHTBLUE_EX}Title: {Style.NORMAL + Fore.LIGHTBLUE_EX + self.title}' \
                       f'{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}\nDate: ' \
                       f'{Style.NORMAL + Fore.LIGHTMAGENTA_EX + self.date}' \
                       f'{Style.BRIGHT + Fore.RED}\nLink: {Style.NORMAL + Fore.RED + self.link}' \
                       f'{Style.BRIGHT + Fore.LIGHTCYAN_EX}\nText: {Style.NORMAL + Fore.LIGHTCYAN_EX + self.text}\n'

            if self.img_links:
                str_item += Style.BRIGHT + Fore.LIGHTRED_EX + 'Image links:\n' + Style.NORMAL + Fore.LIGHTRED_EX

                for num, link in enumerate(self.img_links):
                    str_item += f'\t[{num + 1}]: [{link}]\n'
        else:
            str_item = f'Title: {self.title}' \
                       f'\nDate: {self.date}' \
                       f'\nLink: {self.link}' \
                       f'\nText: {self.text}\n'

            if self.img_links:
                str_item += 'Image links:\n'

                for num, link in enumerate(self.img_links):
                    str_item += f'\t[{num + 1}]: [{link}]\n'

        return str_item
