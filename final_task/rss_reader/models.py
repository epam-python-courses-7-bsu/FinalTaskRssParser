""" Data models module """

from dataclasses import dataclass


@dataclass
class NewsEntry:
    """ Class representing a news article(entry).

        Methods:
        print_entry(self) - print entry in stdout """

    title: str = ""
    summary: str = ""
    date: str = ""
    link: str = ""

    def print_entry(self):
        print("")
        print("-------------------------------------------------------------")
        print("")
        print("Title: " + self.title)
        print("")
        print("Summary: " + self.summary)
        print("")
        print("Publication date: " + self.date)
        print("")
        print("Link: " + self.link)
        print("")
