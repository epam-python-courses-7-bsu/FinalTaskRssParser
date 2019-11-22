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
        self.write_to_pdf(path)

    @logging_decorator
    def option_json(self) -> None:
        for entry in self.entries:
            self.write_cache(self.convert_Entry_to_dict(entry))
            self.print_to_json(self.convert_Entry_to_dict(entry))

    @logging_decorator
    def option_default(self) -> None:
        for entry in self.entries:
            self.print_entry(entry)
            self.write_cache(self.convert_Entry_to_dict(entry))

    @logging_decorator
    def correct_title(self, title: str) -> str:
        return title.replace('"', "_").replace("?", "_").replace(":", "_").replace("'", "_")[:30].replace(" ", "_")

    @logging_decorator
    def write_cache(self, entry_dict: dict):
        """write new news to cache in json format"""
        try:
            entries = json.load(open("cache.json"))
        except json.JSONDecodeError:
            entries = []
        except FileNotFoundError:
            entries = []
        # writing entries and saving images of entries to cache if list of entries with this title is empty
        # else this entry already is the cache
        if not [entry for entry in entries if entry["Title"] == entry_dict["Title"]]:
            entries.append(entry_dict)
            if len(entry_dict["Links"]) > 1:
                self.save_image(entry_dict["Links"][1], self.correct_title(entry_dict["Title"]))

        with open("cache.json", "w") as cache:
            json.dump(entries, cache, indent=2)

    @logging_decorator
    def save_image(self, img_url: str, img_name: str):
        try:
            if img_name.find(".jpg") == -1:
                urllib.request.urlretrieve(img_url, f"images/{img_name}.jpg")
            else:
                urllib.request.urlretrieve(img_url, f"images/{img_name}")
        except FileNotFoundError:
            os.makedirs("images")
            urllib.request.urlretrieve(img_url, f"images/{img_name}.jpg")

    @logging_decorator
    def option_date(self, date: str, do_json: bool, do_html: bool, html_path: str, do_pdf: bool, pdf_path: str):
        """add entries from cache.json into daily_news: list if they have date that is equal to user's --date DATE
            and then raise an exception or print to console or to outputs to html"""
        try:
            entries = json.load(open("cache.json"))
        except json.JSONDecodeError:
            entries = []
        except FileNotFoundError:
            raise RSSReaderException("Error. You have no cache. Try to run app with internet-connection")

        # list of entries with the same date as user's --date DATE
        daily_news = [entry for entry in entries if entry["DateInt"] == date]
        if not daily_news:
            raise RSSReaderException("Error. News aren't found")
        # different cases of command line arguments
        elif do_pdf and do_html:
            self.write_to_pdf(pdf_path, daily_news[:self.limit])
            self.write_entries_to_html(html_path, daily_news[:self.limit])
        elif do_pdf:
            self.write_to_pdf(pdf_path, daily_news[:self.limit])
        elif do_html:
            self.write_entries_to_html(html_path, daily_news[:self.limit])
        elif do_json:
            for news_json in daily_news[:self.limit]:
                self.print_to_json(news_json)
        # default case
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
    def write_entries_to_html(self, path: str, entries=[]) -> None:
        # in case of reading news from cache list of entries are got as dict
        # and in case of online reading news only the path is passed to the method without list of entries
        if os.path.isdir(path) is False:
            raise RSSReaderException("Error. It isn't a folder")
        path = os.path.join(path, "RSS_News.html")

        if not entries:
            entries = self.entries

        html = '<!DOCTYPE html>' \
               '\n<head>\n\t<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n</head>\n<body>'
        # in case of reading news from cache, entries is the list of dicts and they are converted to Entry-object
        if type(entries[0]) == dict:
            entries = [self.get_entry_from_dict(entry) for entry in entries]

        for entry in entries:
            html += '<div style="font-family: Calibri; margin: 5px; padding: 10px;">\n'
            html += '<h1>' + entry.title + '</h1>\n'
            html += '<p>\n<b>Feed:</b> ' + entry.feed + '</p>\n'
            html += '<p>\n<b>Date:</b> ' + entry.date + '</p>\n'

            text = entry.summary
            # adding of an image if the entry has image
            if len(entry.links) > 1:
                alt = text[text.find("image 1: ") + len("image 1: "):text.find(']')]
                while text.count('['):
                    text = text[:text.find('[')] + text[text.find(']') + 1:]
                if text[0] == ' ':
                    text = text[1:]
                html += f'<div style="width: 850px">\n<img alt="{alt}" ' \
                        f'src="file:///{this_dir}/images/{self.correct_title(entry.title)}.jpg" ' \
                        f'style="width: 250px; height: 130px; padding: 0"><p>' + text + '</p>\n</div>\n'
            else:
                # formatting news to more readable format: deleting extra spaces and brackets
                while text.count('['):
                    text = text[:text.find('[')] + text[text.find(']') + 1:]
                if text[0] == ' ':
                    text = text[1:]

                html += '<div style="width: 850px">\n<p>' + text + '</p>\n</div>\n'
            html += '\n</div>'
        html += "</body>\n</html>"

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        except FileNotFoundError:
            raise RSSReaderException('Error. No such folder. Check the correctness of the entered path \n')

    @logging_decorator
    def write_to_pdf(self, path: str, entries=[]) -> None:
        # in case of reading news from cache list of entries are got as dict
        # and in case of online reading news only the path is passed to the method without list of entries
        if os.path.isdir(path) is False:
            raise RSSReaderException("Error. It isn't a folder")
        path = os.path.join(path, "RSS_News.pdf")

        if not entries:
            entries = self.entries

        pdf = PDF()
        pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font("DejaVuSans")
        pdf.alias_nb_pages()
        pdf.add_page()

        # in case of reading news from cache, entries is the list of dicts and they are converted to Entry-object
        if type(entries[0]) == dict:
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
            pdf.set_font_size(14)
            pdf.write(10, f"Date: {entry.date}\n")
            if len(entry.links) > 1:
                try:
                    pdf.image(f'{this_dir}/images/{self.correct_title(entry.title)}.jpg', w=60, h=50)
                except RuntimeError:
                    pass
            pdf.write(10, "\n")
            pdf.write(10, text + "\n\n\n\n")
        pdf.output(path, 'F')
        try:
            pdf.output(path, 'F')
        except FileNotFoundError:
            raise RSSReaderException('Error. No such folder. Check the correctness of the entered path \n')
