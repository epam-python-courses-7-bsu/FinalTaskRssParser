import json
import logging

import feedparser
from Entry import Entry


class Handler:
    """class for handling different options: --version, --json, --limit Limit"""

    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)
        logging.info("Handler object created")

    """options of command line:"""

    def option_version(self) -> None:
        logging.info("function \"option_version\" started")

        print("version ", self.version)

        logging.info("function \"option_version\" finished")

    def option_json(self) -> None:
        logging.info("function \"option_json\" started")

        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            self.print_to_json(self.convert_to_dict(entry))

        logging.info("function \"option_json\" finished")

    def option_default(self) -> None:
        logging.info("function \"option_default\" started")

        self.print_feed()
        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            entry.print_title()
            entry.print_date()
            entry.print_link()
            entry.print_summary()
            entry.print_links()
            if num == self.limit - 1:
                break

        logging.info("function \"option_default\" finished")

    def gen_entries(self) -> Entry:
        """generation instances of Entry class for farther handling them"""
        logging.info("function \"gen_entries\" started")

        for ent in self.parsed.entries:
            entry = Entry(ent.title, ent.published, ent.link, ent.summary, [link["href"] for link in ent.links])
            yield entry

        logging.info("function \"gen_entries\" finished")

    def print_feed(self) -> None:
        logging.info("function \"print_feed\" started")

        print("Feed: ", self.parsed.feed.title, '\n')

        logging.info("function \"print_feed\" finished")

    def print_to_json(self, obj: dict) -> None:
        logging.info("function \"print_to_json\" started")

        print(json.dumps(obj, indent=2))

        logging.info("function \"print_to_json\" finished")

    def convert_to_dict(self, entry: Entry) -> dict:
        logging.info("function \"convert_to_dict\" finished")

        entry_dict = {
            "Feed": self.parsed.feed.title,
            "Title": entry.title,
            "Date": entry.date,
            "Link": entry.article_link,
            "Links": entry.links
        }

        logging.info("function \"convert_to_dict\" finished")
        return entry_dict
