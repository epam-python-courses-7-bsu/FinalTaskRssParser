import logging
import time
from Logging import logging_decorator
import html


class Entry:
    """class for every article from http:link...link.rss"""
    @logging_decorator
    def __init__(self, feed: str = "", title: str = "", date: str = "", article_link: str = "", summary: str = "", links: tuple = (),
                 published_parsed: time.struct_time = ()):
        self.feed = feed
        self.title = self.parse_html(title)
        self.article_link = article_link
        self.links = links
        self.summary = self.parse_html(summary)
        if published_parsed:
            self.publish_year = published_parsed.tm_year
            self.publish_month = published_parsed.tm_mon
            self.publish_day = published_parsed.tm_mday
            # sometimes there is a problem when in the attribute published entries have day that is wrong
            # then code below corrects it and truncates date-string
            self.date = (date[:date.find(",")+2] + str(self.publish_day) + date[date[5:].find(' ') + 5:]
                         )[:len("Fri, 22 Nov 2019")]
        else:
            self.date = date[:len("Fri, 22 Nov 2019")]
        logging.info("Entry object created")

    @logging_decorator
    def print_feed(self) -> None:
        print(f"Feed: {self.feed}\n")

    @logging_decorator
    def print_title(self) -> None:
        print(f"Title: {self.title}")

    @logging_decorator
    def print_date(self) -> None:
        print(f"Date: {self.date}")

    @logging_decorator
    def print_link(self) -> None:
        print(f"Link: {self.article_link}")

    @logging_decorator
    def print_summary(self) -> None:
        print(f"\n{self.summary}\n")

    @logging_decorator
    def print_links(self) -> None:
        print("Links:")
        for num_link, link in enumerate(self.links):
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
                self.links = list(self.links)
                self.links.append(src)
                self.links = tuple(self.links)
            alt = summary[summary.find("alt=\"") + len("alt=\""):
                               summary.find('"', summary.find("alt=\"") + len("alt=\""))
                          ]
            start_cut = summary.find("<img")
            summary = summary[: start_cut] \
                           + f"[image {len(self.links) - 1}: " + alt + "]" \
                           + f"[{len(self.links) - 1}] " \
                           + summary[summary.find(">", start_cut + len("<img")) + 1:]

        while summary.count('<'):
            summary = summary[:summary.find('<')] + summary[summary.find('>') + 1:]

        summary = html.parser.unescape(summary)
        return summary
