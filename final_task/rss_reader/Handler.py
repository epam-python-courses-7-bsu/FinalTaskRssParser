import json
import feedparser
from Entry import Entry


class Handler:
    """class for handling different options: --version, --json, --limit Limit"""

    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)

    """options:"""

    def option_version(self) -> None:
        print("version ", self.version)

    def option_json(self) -> None:
        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            self.print_to_json(self.convert_to_dict(entry))

    def option_default(self) -> None:
        self.print_feed()
        for num, entry in enumerate(self.gen_entries()):
            if num == self.limit:
                break
            entry.print_title()
            entry.print_date()
            entry.print_link()
            entry.print_summary()
            entry.print_links()

    def gen_entries(self) -> Entry:
        """generation instances of Entry class for farther handling them"""
        for ent in self.parsed.entries:
            entry = Entry(ent.title, ent.published, ent.link, ent.summary, [link["href"] for link in ent.links])
            yield entry

    def print_feed(self) -> None:
        print("Feed: ", self.parsed.feed.title, '\n')

    def print_to_json(self, obj: dict) -> None:
        print(json.dumps(obj, indent=2))

    def convert_to_dict(self, entry: Entry) -> dict:
        entry_dict = {
            "Feed": self.parsed.feed.title,
            "Title": entry.title,
            "Date": entry.date,
            "Link": entry.article_link,
            "Links": entry.links
        }
        return entry_dict
