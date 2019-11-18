import json
import dataclasses
from dataclasses import dataclass


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
        str_for_print = f"Feed: {self.feed}\n" \
                        f"Title: {self.title}\n" \
                        f"Date: {self.date}\n" \
                        f"Link: {self.link}\n" \
                        f"{self.summary}\n"
        for index, value in enumerate(self.links, 1):
            str_for_print += f"[{index}]: {value[0]}\n"
        return str_for_print
