from dataclasses import dataclass


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
        """selects alt and src attributes from <img> and removes all the html tags from the entry.summary"""
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