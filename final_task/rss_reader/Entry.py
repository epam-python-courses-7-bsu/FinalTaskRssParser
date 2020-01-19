import logging
import time
from Logging import logging_decorator
import html
from html import parser


class Entry:
    """class for every article from http:link...link.rss"""
    @logging_decorator
    def __init__(self, feed: str = "", title: str = "", date: str = "", article_link: str = "",
                 summary: str = "", links: tuple = (), published_parsed: time.struct_time = ()):
        self.__feed = feed
        self.__title = self.parse_html(title)
        self.__article_link = article_link
        self.__links = links
        self.__summary = self.parse_html(summary)
        if published_parsed:
            self.__publish_year = published_parsed.tm_year
            self.__publish_month = published_parsed.tm_mon
            self.__publish_day = published_parsed.tm_mday
            # sometimes there is a problem when in the attribute published entries have day that is wrong
            # then code below corrects it and truncates date-string
            self.__date = (date[:date.find(",")+2] + str(self.__publish_day) + date[date[5:].find(' ') + 5:]
                         )[:len("Fri, 22 Nov 2019")]
        else:
            self.__date = date[:len("Fri, 22 Nov 2019")]
        logging.info("Entry object created")

    @logging_decorator
    def get_feed(self) -> str:
        return self.__feed

    @logging_decorator
    def get_title(self) -> str:
        return self.__title

    @logging_decorator
    def get_article_link(self) -> str:
        return self.__article_link

    @logging_decorator
    def get_links(self) -> tuple:
        return self.__links

    @logging_decorator
    def get_summary(self) -> str:
        return self.__summary

    @logging_decorator
    def get_publish_year(self):
        return self.__publish_year

    @logging_decorator
    def get_publish_month(self):
        return self.__publish_month

    @logging_decorator
    def get_publish_day(self):
        return self.__publish_day

    @logging_decorator
    def get_date(self) -> str:
        return self.__date

    @logging_decorator
    def print_feed(self) -> None:
        print(f"Feed: {self.__feed}\n")

    @logging_decorator
    def print_title(self) -> None:
        print(f"Title: {self.__title}")

    @logging_decorator
    def print_date(self) -> None:
        print(f"Date: {self.__date}")

    @logging_decorator
    def print_link(self) -> None:
        print(f"Link: {self.__article_link}")

    @logging_decorator
    def print_summary(self) -> None:
        print(f"\n{self.__summary}\n")

    @logging_decorator
    def print_links(self) -> None:
        print("Links:")
        for num_link, link in enumerate(self.__links):
            if num_link == 0:
                print(f'[{num_link}] {link} (link)')
            else:
                print(f'[{num_link}] {link} (image)')
        print('\n')

    @logging_decorator
    def parse_html(self, summary: str) -> str:
        """selects alt and src attributes from <img> and removes all the html tags from the entry.summary"""
        while summary.count('<img'):
            src = summary[summary.find("src=\"") + len("src=\""):
                               summary.find('"', summary.find("src=\"") + len("src=\""))
                          ]
            if src != "":
                self.__links = list(self.__links)
                self.__links.append(src)
                self.__links = tuple(self.__links)
            alt = summary[summary.find("alt=\"") + len("alt=\""):
                               summary.find('"', summary.find("alt=\"") + len("alt=\""))
                          ]
            start_cut = summary.find("<img")
            summary = summary[: start_cut] \
                           + f"[image {len(self.__links) - 1}: " + alt + "]" \
                           + f"[{len(self.__links) - 1}] " \
                           + summary[summary.find(">", start_cut + len("<img")) + 1:]

        while summary.count('<'):
            summary = summary[:summary.find('<')] + summary[summary.find('>') + 1:]

        summary = html.parser.unescape(summary)
        return summary
