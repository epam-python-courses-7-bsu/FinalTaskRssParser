import json
import feedparser
import argparse
from dataclasses import dataclass


@dataclass
class ArgParser:
    """class for reading console arguments"""
    source: str = ""
    status_version: bool = False
    status_json: bool = False
    status_verbose: bool = False
    limit: int = 1

    arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    arg_parser.add_argument("source", type=str, help="RSS URL")
    arg_parser.add_argument("--version", action="store_true", help="Print version info")
    arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument("--limit", type=int, default=1, help="Limit news topics if this parameter provided")
    arg_parser_args = arg_parser.parse_args()

    def __post_init__(self):
        self.source = self.arg_parser_args.source
        self.status_version = self.arg_parser_args.version
        self.status_json = self.arg_parser_args.json
        self.status_verbose = self.arg_parser_args.verbose
        self.limit = self.arg_parser_args.limit


@dataclass
class Entry:
    """class for every article from http:link...link.rss"""
    title: str
    date: str
    article_link: str
    summary: str
    links: list

    def __post_init__(self):
        self.parse_html()

    def print_title(self) -> None:
        print("Title: ", self.title)

    def print_date(self) -> None:
        print("Date: ", self.date)

    def print_link(self) -> None:
        print("Link: ", self.article_link)

    def print_summary(self) -> None:
        print('\n')
        print(self.summary)
        print('\n')

    def print_links(self) -> None:
        print("Links:")
        for i, link in enumerate(self.links):
            print(f'[{i}] ', link)
        print('\n')

    def parse_html(self) -> None:
        """selects alt and src attributes from <img> and removes all the html tags from the entry.summary"""
        while self.summary.count('<img'):
            src = self.summary[self.summary.find("src=\"") + len("src=\""):
                                self.summary.find('"', self.summary.find("src=\"") + len("src=\""))
                  ]
            self.links.append(src)
            alt = self.summary[self.summary.find("alt=\"") + len("alt=\""):
                                self.summary.find('"', self.summary.find("alt=\"") + len("alt=\""))
                  ]
            start_cut = self.summary.find("<img")
            self.summary = self.summary[: start_cut] \
                            + f"[image {len(self.links) - 1}: " + alt + "]" \
                            + f"[{len(self.links) - 1}] " \
                            + self.summary[self.summary.find(">", start_cut + len("<img")) + 1:]

        while self.summary.count('<'):
            self.summary = self.summary[:self.summary.find('<')] + self.summary[self.summary.find('>') + 1:]


@dataclass()
class Handler:
    """class for handling different options: --version, --json, --limit Limit"""
    source: str
    limit: int
    version: float

    def __post_init__(self):
        self.parsed = feedparser.parse(self.source)

    """options:"""
    def option_version(self) -> None:
        print("version ", self.version)

    def option_json(self) -> None:
        self.print_feed()
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


def main():
    version = 1.0
    arg_parser = ArgParser()
    handler = Handler(arg_parser.source, arg_parser.limit, version)

    try:
        if arg_parser.status_version:
            handler.option_version()
        elif arg_parser.status_json:
            handler.option_json()
        else:
            handler.option_default()
    except AttributeError:
        print("Error, failed to get an attribute. Check correctness URL")


if __name__ == "__main__":
    main()
