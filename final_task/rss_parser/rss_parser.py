import json
import feedparser
import argparse
from dataclasses import dataclass

version = 1.0


@dataclass
class ArgParser:
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
    title: str
    date: str
    article_link: str
    summary: str
    links: list

    def __post_init__(self):
        self.parse_html()

    def print_title(self):
        print("Title: ", self.title)

    def print_date(self):
        print("Date: ", self.date)

    def print_link(self):
        print("Link: ", self.article_link)

    def print_summary(self):
        print('\n')
        print(self.summary)
        print('\n')

    def print_links(self):
        print("Links:")
        for i, link in enumerate(self.links):
            print(f'[{i}] ', link)
        print('\n')

    def parse_html(self):
        """selects alt and src attributes from <img> and removes all the html tags from the entry"""
        while self.summary.count('<img'):
            src = self.summary[self.summary.find("src=\"") + len("src=\""):
                                self.summary.find('"', self.summary.find("src=\"") + len("src=\""))
                  ]
            self.links.append({"href": src})
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
    parsed: dict

    def print_feed(self):
        print("Feed: ", self.parsed.feed.title, '\n')
# def gen_entries(parsed):
#     for entr in parsed.entries:
#         yield entr


# def print_feed(parsed):
#     print("Feed: ", parsed.feed.title, '\n')


# def print_entry_title(entry):
#     print("Title: ", entry.title)
#
#
# def print_entry_date(entry):
#     print("Date: ", entry.published)
#
#
# def print_entry_link(entry):
#     print("Link: ", entry.link, '\n')
#
#
# def print_links_entry(entry):
#     print("Links:")
#     for i, link in enumerate(entry.links):
#         print(f'[{i}] ', link["href"])
#     print('\n')


# def print_entry(entry):
#     print_entry_title(entry)
#     print_entry_date(entry)
#     print_entry_link(entry)
#     print(entry.summary, '\n')
#     print_links_entry(entry)


# def print_entries(parsed, a: ArgParser):
#     for num, entry in enumerate(parsed.entries):
#         if num == a.limit:
#             break
#         parse_html(entry)
#         print_entry(entry)


def print_to_json(obj):
    print(json.dumps(obj, indent=2))


# def parse_html(entry):
#     """selects alt and src attributes from <img> and removes all the html tags from the entry"""
#     while entry.summary.count('<img'):
#         src = entry.summary[entry.summary.find("src=\"") + len("src=\""):
#                             entry.summary.find('"', entry.summary.find("src=\"") + len("src=\""))
#               ]
#         entry.links.append({"href": src})
#         alt = entry.summary[entry.summary.find("alt=\"") + len("alt=\""):
#                             entry.summary.find('"', entry.summary.find("alt=\"") + len("alt=\""))
#               ]
#         start_cut = entry.summary.find("<img")
#         entry.summary = entry.summary[: start_cut] \
#                         + f"[image {len(entry.links) - 1}: " + alt + "]" \
#                         + f"[{len(entry.links) - 1}] " \
#                         + entry.summary[entry.summary.find(">", start_cut + len("<img")) + 1:]
#
#     while entry.summary.count('<'):
#         entry.summary = entry.summary[:entry.summary.find('<')] + entry.summary[entry.summary.find('>') + 1:]


def convert_to_dict(parsed, entry):
    entry_dict = {
        "Feed": parsed.feed.title,
        "Title": entry.title,
        "Date": entry.published,
        "Link": entry.link,
        "Links": [link["href"] for link in entry.links]
    }
    return entry_dict


"""execution options: json, version, limit ..."""


def case_json(source, limit):
    parsed = feedparser.parse(source)
    print_feed(parsed)
    gen = gen_entries(parsed)
    for num, entry in enumerate(gen):
        if num == limit:
            break
        print_to_json(convert_to_dict(parsed, entry))


def gen_entries(parsed):
    for ent in parsed.entries:
        entry = Entry(ent.title, ent.published, ent.link, ent.summary, [link["href"] for link in ent.links])
        yield entry


def case_default(source, limit):
    parsed = feedparser.parse(source)
    print_feed(parsed)
    for num, entry in enumerate(gen_entries(parsed)):
        if num == limit:
            break
        entry.print_title()
        entry.print_date()
        entry.print_link()
        entry.print_summary()
        entry.print_links()

def case_version():
    print("version ", version)


# """arguments from cl"""
# arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
# arg_parser.add_argument("source", type=str, help="RSS URL")
# arg_parser.add_argument("--version", action="store_true", help="Print version info")
# arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
# arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
# arg_parser.add_argument("--limit", type=int, default=1, help="Limit news topics if this parameter provided")
# arg_parser_args = arg_parser.parse_args()


def main():
    a = ArgParser()
    try:
        if a.status_version:
            case_version()
        elif a.status_json:
            case_json(a)
        else:
            case_default(a.source, a.limit)
    except AttributeError:
        print("Error, failed to get an attribute. Check correctness URL")


if __name__ == "__main__":
    main()
