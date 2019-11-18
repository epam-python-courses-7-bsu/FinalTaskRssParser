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
        print("-------------------------------------------------------------",
              "Title: " + self.title + '\n',
              "Summary: " + self.summary + '\n',
              "Publication date: " + self.date + '\n',
              "Link: " + self.link + '\n',
              sep='\n')
