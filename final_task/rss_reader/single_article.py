import json
import dataclasses
from dataclasses import dataclass

import colorizing_handler

from termcolor import colored


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, data_class):
        if dataclasses.is_dataclass(data_class):
            return dataclasses.asdict(data_class)
        return super().default(data_class)


@dataclass
class SingleArticle:
    feed: str
    feed_url: str
    title: str
    date: str
    link: str
    summary: str
    links: list

    def __str__(self) -> str:
        """Makes str with data of instance of a class"""
        if not colorizing_handler.COLORIZING_STATUS:
            str_for_print = f"Feed: {self.feed}\n" \
                            f"Title: {self.title}\n" \
                            f"Date: {self.date}\n" \
                            f"Link: {self.link}\n" \
                            f"{self.summary}\n"
            for index, value in enumerate(self.links, 1):
                str_for_print += f"[{index}]: {value[0]}\n"
        else:
            str_for_print = f"{colored('Feed: ', 'yellow', attrs=['bold'])}" \
                            f"{colored(f' {self.feed}', 'magenta', attrs=['bold'])}\n" \
                            f"{colored('Title:', 'yellow', attrs=['bold'])}" \
                            f"{colored(f' {self.title}', 'cyan', attrs=['bold'])}\n" \
                            f"{colored('Date: ', 'yellow', attrs=['bold'])}" \
                            f"{colored(f' {self.date}', 'green', attrs=['bold'])}\n" \
                            f"{colored('Link: ', 'yellow', attrs=['bold'])}" \
                            f"{colored(f' {self.link}', 'blue', attrs=['bold'])}\n" \
                            f"{colored(f'{self.summary}', 'white', attrs=['bold'])}\n"
            for index, value in enumerate(self.links, 1):
                str_for_print += f"{colored(f'[{index}]:', 'yellow')}" \
                                 f"{colored(f' {value[0]}', 'blue', attrs=['bold'])}\n"

        return str_for_print
