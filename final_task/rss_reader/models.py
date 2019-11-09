""" Data models module """
import argparse


class ArgReader:
    """ Class for receiving command line arguments.

        Class stores the arguments of an instance
        of the ArgumentParser class in its fields """
    version: bool
    json: bool
    limit: int
    source: str
    verbose: bool

    def __init__(self):
        parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.", add_help=True)
        parser.add_argument("source", type=str, help="RSS URL")
        parser.add_argument("--version", action="store_true", help="Print version info")
        parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
        parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
        parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

        parser.parse_args(namespace=self)


class NewsEntry:
    """ Class representing a news article(entry).

        Methods:
        print_entry(self) - print entry in stdout """

    title: str
    summary: str
    date: str
    link: str

    def print_entry(self):
        print()
        print("-------------------------------------------------------------")
        print()
        print("Title: " + self.title)
        print()
        print("Summary: " + self.summary)
        print()
        print("Publication date: " + self.date)
        print()
        print("Link: " + self.link)
