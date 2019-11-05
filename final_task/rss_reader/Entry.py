import logging


class Entry:
    """class for every article from http:link...link.rss"""

    def __init__(self, title: str, date: str, article_link: str, summary: str, links: list):
        self.title = title
        self.date = date
        self.article_link = article_link
        self.summary = summary
        self.links = links
        self.parse_html()
        logging.info("Entry object created")

    def print_title(self) -> None:
        logging.info("function \"print_title\" started")

        print("Title: ", self.title)

        logging.info("function \"print_title\" finished")

    def print_date(self) -> None:
        logging.info("function \"print_date\" started")

        print("Date: ", self.date)

        logging.info("function \"print_date\" finished")

    def print_link(self) -> None:
        logging.info("function \"print_link\" started")

        print("Link: ", self.article_link)

        logging.info("function \"print_link\" finished")

    def print_summary(self) -> None:
        logging.info("function \"print_summary\" started")

        print('\n')
        print(self.summary)
        print('\n')

        logging.info("function \"print_summary\" finished")

    def print_links(self) -> None:
        logging.info("function \"print_links\" started")

        print("Links:")
        for num_link, link in enumerate(self.links):
            print(f'[{num_link}] ', link)
        print('\n')

        logging.info("function \"print_links\" finished")

    def parse_html(self) -> None:
        logging.info("function \"parse_html\" started")

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

        logging.info("function \"parse_html\" finished")
