import logging
from Logging import logging_decorator


class Entry:
    """class for every article from http:link...link.rss"""
    @logging_decorator
    def __init__(self, title: str, date: str, article_link: str, summary: str, links: list):
        self.title = self.parse_html(title)
        self.date = date
        self.article_link = article_link
        self.links = links
        self.summary = self.parse_html(summary)
        logging.info("Entry object created")

    @logging_decorator
    def print_title(self) -> None:
        print("Title: ", self.title)

    @logging_decorator
    def print_date(self) -> None:
        print("Date: ", self.date)

    @logging_decorator
    def print_link(self) -> None:
        print("Link: ", self.article_link)

    @logging_decorator
    def print_summary(self) -> None:
        print('\n')
        print(self.summary)
        print('\n')

    @logging_decorator
    def print_links(self) -> None:
        print("Links:")
        for num_link, link in enumerate(self.links):
            if num_link == 0:
                print(f'[{num_link}] ', link, "(link)")
            else:
                print(f'[{num_link}] ', link, "(image)")
        print('\n')

    @logging_decorator
    def parse_html(self, summary: str) -> str:
        """selects alt and src attributes from <img> and removes all the html tags from the entry.summary"""
        while summary.count('<img'):
            src = summary[summary.find("src=\"") + len("src=\""):
                               summary.find('"', summary.find("src=\"") + len("src=\""))
                          ]
            if src != "":
                self.links.append(src)
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

        # decode special symbols:
        for symbol in ['&iquest;', '&iexcl;', '&laquo;', '&raquo;', '&lsaquo;', '&rsaquo;', '&quot;', '&lsquo;',
                    '&rsquo;', '&ldquo;', '&rdquo;', '&sbquo;', '&bdquo;', '&sect;', '&para;', '&dagger;',
                    '&Dagger;', '&bull;', '&mdash;', '&ndash;', '&hellip;', '&nbsp;'
                    ]:
            while summary.count(symbol):
                summary = summary[:summary.find(symbol)] + '"' + summary[summary.find(symbol) + len(symbol):]
        # decode ASCII codes:
        while summary.count("&#"):
            code = summary[summary.find("&#") + 2: summary.find(";")]
            summary = summary[:summary.find("&#")] + chr(int(code)) + summary[summary.find("&#") + 3 + len(code):]

        return summary
