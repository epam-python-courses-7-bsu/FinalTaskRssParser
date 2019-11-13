import json
import logging
from itertools import islice
from json import JSONDecodeError

import feedparser
from Entry import Entry
from Logging import logging_decorator
from RSSReaderException import RSSReaderException


class Handler:
    """class for handling different options: --version, --json, --limit Limit, --date"""
    @logging_decorator
    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)
        logging.info("Handler object created")

    # options of command line:
    @logging_decorator
    def option_version(self) -> None:
        print("version ", self.version)

    @logging_decorator
    def option_json(self) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.print_to_json(self.convert_to_dict(entry))
            self.write_json_to_cache(self.convert_to_dict(entry))

    @logging_decorator
    def option_default(self) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.print_entry(entry)

            self.write_json_to_cache(self.convert_to_dict(entry))

    @logging_decorator
    def write_json_to_cache(self, entry_dict):
        try:
            entries = json.load(open("cache.json"))
        except JSONDecodeError:
            entries = []

        if not [entry for entry in entries if entry["Title"] == entry_dict["Title"]]:
            entries.append(entry_dict)

        with open("cache.json", "w") as cache:
            json.dump(entries, cache, indent=2)

    @logging_decorator
    # read entries from cache.json into list daily_news that have date that is equal to --date DATE
    # and then raise an exception or print to console
    def option_date(self, date: str, do_json: bool):
        try:
            entries = json.load(open("cache.json"))
        except JSONDecodeError:
            entries = []

        daily_news = [entry for entry in entries if entry["DateInt"] == date]

        if not daily_news:
            raise RSSReaderException("Error. News aren't found")
        elif do_json:
            for news in daily_news[:self.limit]:
                self.print_to_json(news)
        else:
            for news in daily_news[:self.limit]:
                entry = self.get_entry_from_dict(news)
                self.print_entry(entry)

    @logging_decorator
    def print_entry(self, entry: Entry) -> None:
        entry.print_feed()
        entry.print_title()
        entry.print_date()
        entry.print_link()
        entry.print_summary()
        entry.print_links()

    @logging_decorator
    def get_entry_from_dict(self, entry_dict: dict) -> Entry:
        return Entry(entry_dict["Feed"], entry_dict["Title"], entry_dict["Date"], entry_dict["Link"], entry_dict["Summary"],
                     entry_dict["Links"])

    @logging_decorator
    def gen_entries(self) -> Entry:
        """generation instances of Entry class for farther handling them"""
        for ent in self.parsed.entries:
            entry = Entry(self.parsed.feed.title, ent.title, ent.published, ent.link, ent.summary, tuple([link["href"] for link in ent.links]),
                          ent.published_parsed)
            yield entry

    @logging_decorator
    def print_to_json(self, obj: dict) -> None:
        print(json.dumps(obj, indent=2))

    @logging_decorator
    def convert_to_dict(self, entry: Entry) -> dict:
        entry_dict = {
            "Feed": entry.feed,
            "Title": entry.title,
            "DateInt": str(entry.publish_year) + str(entry.publish_month) + str(entry.publish_day),
            "Date": entry.date,
            "Link": entry.article_link,
            "Summary": entry.summary,
            "Links": entry.links,
        }
        return entry_dict
