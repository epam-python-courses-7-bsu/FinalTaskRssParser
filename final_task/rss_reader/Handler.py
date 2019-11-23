import json
import logging
import os
import sys
this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)
import feedparser
from Entry import Entry
from Logging import logging_decorator
from RSSReaderException import RSSReaderException
from RSS_PDF import PDF
import urllib.request
from dominate.tags import html, head, meta, body, div, img, p, b, br, h1, a


class Handler:
    """class for handling different options: --version, --json, --limit Limit, --date"""

    @logging_decorator
    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)
        self.entries = []
        for ent in self.parsed.entries[:self.limit]:
            self.entries.append(Entry(
                self.parsed.feed.title, ent.title, ent.published, ent.link, ent.summary,
                tuple([link["href"] for link in ent.links]), ent.published_parsed)
            )
        logging.info("Handler object created")

    # options of command line:
    @logging_decorator
    def option_version(self) -> None:
        print("version ", self.version)

    @logging_decorator
    def option_html(self, path: str) -> None:
        for entry in self.entries:
            self.write_cache(self.convert_Entry_to_dict(entry))
        self.write_entries_to_html(path)

    @logging_decorator
    def option_pdf(self, path: str) -> None:
        for entry in self.entries:
            self.write_cache(self.convert_Entry_to_dict(entry))
        self.write_entries_to_pdf(path)

    @logging_decorator
    def option_json(self) -> None:
        for entry in self.entries:
            self.write_cache(self.convert_Entry_to_dict(entry))
            self.print_to_json(self.convert_Entry_to_dict(entry))

    @logging_decorator
    def option_default(self) -> None:
        for entry in self.entries:
            self.write_cache(self.convert_Entry_to_dict(entry))
            self.print_entry(entry)

    @logging_decorator
    def correct_title(self, title: str) -> str:
        return title.replace('"', "_").replace("?", "_").replace(":", "_").replace("'", "_").replace(" ", "_")[:30]

    @logging_decorator
    def write_cache(self, entry_dict: dict) -> None:
        """write new news to cache in json format"""
        if os.path.exists("cache.json"):
            try:
                with open("cache.json") as cache:
                    entries = json.load(cache)
            except json.JSONDecodeError:
                entries = []
        else:
            entries = []
        # writing entries and saving images of entries to cache if list of entries with this title is empty
        # else this entry already is the cache
        if not [entry for entry in entries if entry["Title"] == entry_dict["Title"]]:
            entries.append(entry_dict)
            if len(entry_dict["Links"]) > 1:
                for num_img_l, img_l in enumerate(entry_dict["Links"][1:]):
                    self.save_image(img_l, self.correct_title(entry_dict["Title"]) + str(num_img_l))

        with open("cache.json", "w") as cache:
            json.dump(entries, cache, indent=2)

    @logging_decorator
    def save_image(self, img_url: str, img_name: str) -> None:
        if os.path.exists("images"):
            if img_name.find(".jpg") == -1:
                urllib.request.urlretrieve(img_url, f"images/{img_name}.jpg")
            else:
                urllib.request.urlretrieve(img_url, f"images/{img_name}")
        else:
            os.makedirs("images")
            urllib.request.urlretrieve(img_url, f"images/{img_name}.jpg")

    @logging_decorator
    def option_date(self, date: str, do_json: bool, html_path: str = "", pdf_path: str = ""):
        """add entries from cache.json into daily_news: list if they have date that is equal to user's --date DATE
            and then raise an exception or print to console or to outputs to html"""
        if os.path.exists("cache.json"):
            try:
                with open("cache.json") as cache:
                    entries = json.load(cache)
            except json.JSONDecodeError:
                entries = []
        else:
            raise RSSReaderException("Error. You have no cache. Try to run app with internet-connection")

        # list of entries with the same date as user's --date DATE
        daily_news = [entry for entry in entries if entry["DateInt"] == date]
        if not daily_news:
            raise RSSReaderException("Error. News aren't found")
        # different cases of command line arguments
        if pdf_path:
            self.write_entries_to_pdf(pdf_path, daily_news[:self.limit])
        if html_path:
            self.write_entries_to_html(html_path, daily_news[:self.limit])
        if do_json:
            for news_json in daily_news[:self.limit]:
                self.print_to_json(news_json)
        # default case
        if not (pdf_path or html_path or do_json):
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
        return Entry(entry_dict["Feed"], entry_dict["Title"], entry_dict["Date"], entry_dict["Link"],
                     entry_dict["Summary"], entry_dict["Links"])

    @logging_decorator
    def print_to_json(self, obj: dict) -> None:
        print(json.dumps(obj, indent=2))

    @logging_decorator
    def convert_Entry_to_dict(self, entry: Entry) -> dict:
        return {
            "Feed": entry.feed,
            "Title": entry.title,
            "DateInt": str(entry.publish_year) + str(entry.publish_month) + str(entry.publish_day),
            "Date": entry.date,
            "Link": entry.article_link,
            "Summary": entry.summary,
            "Links": entry.links
        }

    @logging_decorator
    def write_entries_to_html(self, path: str, entries=()) -> None:
        # in case of reading news from cache list of entries are got as dict
        # and in case of online reading news only the path is passed to the method without list of entries
        if os.path.isdir(path) is False:
            raise RSSReaderException("Error. It isn't a folder")

        if not entries:
            entries = self.entries

        if isinstance(entries[0], dict):
            entries = [self.get_entry_from_dict(entry) for entry in entries]

        _html = html()
        _html.add(head(meta(charset='utf-8')))
        _body = _html.add(body())
        with _body:
            for entry in entries:
                _div = _body.add(div())
                _div += h1(entry.title)
                _div += p(b("Feed: "), a(entry.feed))
                _div += p(b("Date: "), a(entry.date))

                text = entry.summary
                # adding of an image if the entry has image
                if len(entry.links) > 1:
                    while text.count('['):
                        text = text[:text.find('[')] + text[text.find(']') + 1:]
                    if text[0] == ' ':
                        text = text[1:]
                    for num_img_l in range(len(entry.links[1:])):
                        _div += img(src=f"file:///{this_dir}/images/"
                                        f"{self.correct_title(entry.title)+str(num_img_l)}.jpg")
                        _div += br(), br()
                else:
                    # formatting news to more readable format: deleting extra spaces and brackets
                    while text.count('['):
                        text = text[:text.find('[')] + text[text.find(']') + 1:]
                    if text[0] == ' ':
                        text = text[1:]

                import html.parser as html_parser
                _div += p(html_parser.unescape(text), br(), br())

        if os.path.exists(path):
            path = os.path.join(path, "RSS_News.html")
            with open(path, 'w', encoding='utf-8') as rss_html:
                rss_html.write(str(_html))
        else:
            raise RSSReaderException('Error. No such folder. Check the correctness of the entered path \n')

    @logging_decorator
    def write_entries_to_pdf(self, path: str, entries=()) -> None:
        # in case of reading news from cache list of entries are got as dict
        # and in case of online reading news only the path is passed to the method without list of entries
        if os.path.isdir(path) is False:
            raise RSSReaderException("Error. It isn't a folder")

        if not entries:
            entries = self.entries

        pdf = PDF()
        pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font("DejaVuSans")
        pdf.alias_nb_pages()
        pdf.add_page()

        # in case of reading news from cache, entries is the list of dicts and they are converted to Entry-object
        if isinstance(entries[0], dict):
            entries = [self.get_entry_from_dict(entry) for entry in entries]
        for entry in entries:
            text = entry.summary
            # adding of an image if the entry has image
            if len(entry.links) > 1:
                while text.count('['):
                    text = text[:text.find('[')] + text[text.find(']') + 1:]
                if text[0] == ' ':
                    text = text[1:]
            else:
                # formatting news to more readable format: deleting extra spaces and brackets
                while text.count('['):
                    text = text[:text.find('[')] + text[text.find(']') + 1:]
                if text[0] == ' ':
                    text = text[1:]

            pdf.set_font_size(24)
            pdf.write(10, entry.title + '\n\n')
            pdf.set_font_size(14)
            pdf.write(10, f"Feed: {entry.feed}\n")
            pdf.write(10, f"Date: {entry.date}\n")
            if len(entry.links) > 1:
                try:
                    for num_img_l in range(len(entry.links[1:])):
                        pdf.image(f'{this_dir}/images/{self.correct_title(entry.title)+str(num_img_l)}.jpg', w=60, h=50)
                        pdf.write(10, "\n")
                except RuntimeError:
                    pass
            pdf.write(10, "\n")
            pdf.write(10, text + "\n\n\n\n")

        if os.path.exists(path):
            path = os.path.join(path, "RSS_News.pdf")
            pdf.output(path, 'F')
        else:
            raise RSSReaderException('Error. No such folder. Check the correctness of the entered path \n')
