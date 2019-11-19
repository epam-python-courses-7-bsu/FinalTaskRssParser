import json
import logging
from itertools import islice
import feedparser
from Entry import Entry
from Logging import logging_decorator
from RSSReaderException import RSSReaderException


class Handler:
    """class for handling different options: --version, --json, --limit Limit, --date"""
    @logging_decorator
    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)
        logging.info("Handler object created")

    # options of command line:
    @logging_decorator
    def option_version(self) -> None:
        print("version ", self.version)

    @logging_decorator
    def option_html(self, path: str) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.write_to_html(entry, path)

    @logging_decorator
    def option_json(self) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.print_to_json(self.convert_to_dict(entry))
            self.write_json_to_cache(self.convert_to_dict(entry))

    @logging_decorator
    def option_default(self) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.print_entry(entry)

            self.write_json_to_cache(self.convert_to_dict(entry))

    @logging_decorator
    def write_json_to_cache(self, entry_dict):
        try:
            entries = json.load(open("cache.json"))
        except json.JSONDecodeError:
            entries = []

        if not [entry for entry in entries if entry["Title"] == entry_dict["Title"]]:
            entries.append(entry_dict)

        with open("cache.json", "w") as cache:
            json.dump(entries, cache, indent=2)

    @logging_decorator
    def option_date(self, date: str, do_json: bool, do_html: bool, html_path: str):
        """read entries from cache.json into list daily_news that have date that is equal to --date DATE
            and then raise an exception or print to console"""
        try:
            entries = json.load(open("cache.json"))
        except json.JSONDecodeError:
            entries = []
        except FileNotFoundError:
            raise RSSReaderException("Error. You have no cache. Try to run app with internet-connection")

        daily_news = [entry for entry in entries if entry["DateInt"] == date]

        if not daily_news:
            raise RSSReaderException("Error. News aren't found")
        elif do_html:
            for news in daily_news[:self.limit]:
                self.write_to_html(self.get_entry_from_dict(news), html_path)
        elif do_json:
            for news in daily_news[:self.limit]:
                self.print_to_json(news)
        else:
            for news in daily_news[:self.limit]:
                entry = self.get_entry_from_dict(news)
                self.print_entry(entry)

    @logging_decorator
    def print_entry(self, entry: Entry) -> None:
        entry.print_feed()
        entry.print_title()
        entry.print_date()
        entry.print_link()
        entry.print_summary()
        entry.print_links()

    @logging_decorator
    def get_entry_from_dict(self, entry_dict: dict) -> Entry:
        return Entry(entry_dict["Feed"], entry_dict["Title"], entry_dict["Date"], entry_dict["Link"], entry_dict["Summary"],
                     entry_dict["Links"])

    @logging_decorator
    def gen_entries(self) -> Entry:
        """generation instances of Entry class for farther handling them"""
        for ent in self.parsed.entries:
            entry = Entry(self.parsed.feed.title, ent.title, ent.published, ent.link, ent.summary, tuple([link["href"] for link in ent.links]),
                          ent.published_parsed)
            yield entry

    @logging_decorator
    def print_to_json(self, obj: dict) -> None:
        print(json.dumps(obj, indent=2))

    @logging_decorator
    def convert_to_dict(self, entry: Entry) -> dict:
        entry_dict = {
            "Feed": entry.feed,
            "Title": entry.title,
            "DateInt": str(entry.publish_year) + str(entry.publish_month) + str(entry.publish_day),
            "Date": entry.date,
            "Link": entry.article_link,
            "Summary": entry.summary,
            "Links": entry.links,
        }
        return entry_dict

    @logging_decorator
    def write_to_html(self, entry: Entry, path: str) -> None:
        try:
            if path[-1] != '/':
                path += '/'
        except IndexError:
            raise IndexError

        if path.find(".html") == -1:
            path += "index.html"
        else:
            raise RSSReaderException("Error. It isn't a folder")

        html = '<div style="font-family: Calibri; margin: 5px; padding: 10px;">\n'
        html += '<h1>' + entry.title + '</h1>\n'
        html += '<p>\n<b>Feed:</b> ' + entry.feed + '</p>\n'
        html += '<p>\n<b>Date:</b> ' + entry.date + '</p>\n'

        # extract src and alt attributes from field Entry.summary
        text = entry.summary
        if len(entry.links) > 1:
            alt = text[text.find("image 1: ") + len("image 1: "):text.find(']')]
            src = entry.links[1]
            while text.count('['):
                text = text[:text.find('[')] + text[text.find(']') + 1:]
            if text[0] == ' ':
                text = text[1:]
            html += f'<div style="width: 850px">\n<img alt="{alt}" src="{src}" ' \
                    f'style="width: 250px; height: 130px; padding: 0"><p>' + text + '</p>\n</div>\n'
        else:
            html += '<div style="width: 850px">\n<p>' + text + '</p>\n</div>\n'
        html += '\n</div>'

        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(html)
        except FileNotFoundError:
            raise RSSReaderException('Error. No such folder. Check the correctness of the entered path \n')
