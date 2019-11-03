import json
from dataclasses import dataclass
import feedparser

from rss_parser.Entry import Entry


@dataclass()
class Handler:
    """class for handling different options: --version, --json, --limit Limit"""
    source: str
    limit: int
    version: float

    def __post_init__(self):
        self.parsed = feedparser.parse(self.source)

    """options:"""
    def option_version(self):
        print("version ", self.version)

    def option_json(self):
        self.print_feed()
        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            self.print_to_json(self.convert_to_dict(entry))

    def option_default(self):
        self.print_feed()
        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            entry.print_title()
            entry.print_date()
            entry.print_link()
            entry.print_summary()
            entry.print_links()

    def gen_entries(self):
        """generation instances of Entry class for farther handling them"""
        for ent in self.parsed.entries:
            entry = Entry(ent.title, ent.published, ent.link, ent.summary, [link["href"] for link in ent.links])
            yield entry

    def print_feed(self):
        print("Feed: ", self.parsed.feed.title, '\n')

    def print_to_json(self, obj: dict):
        print(json.dumps(obj, indent=2))

    def convert_to_dict(self, entry: Entry):
        entry_dict = {
            "Feed": self.parsed.feed.title,
            "Title": entry.title,
            "Date": entry.date,
            "Link": entry.article_link,
            "Links": entry.links
        }
        return entry_dict
