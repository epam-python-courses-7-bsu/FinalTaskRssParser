import os
import sys
import unittest
out_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(out_dir)
from Handler import Handler
from Entry import Entry
from RSSReaderException import RSSReaderException


class TestHandler(unittest.TestCase):
    def test__init__(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertIsInstance(handler, Handler)
        self.assertNotIsInstance("handler", Handler)

    def test_gen_entries(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertIsInstance(next(handler.gen_entries()), Entry)

    def test_convert_to_dict(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        entry = Entry("Yahoo News - Latest News & Headlines", "Title 1", "Wed, 06 Nov 2019 14:22:10 +0500",
                      "https://link1.com", "summary", ("https://link1.com",))
        entry.publish_year = 2019
        entry.publish_month = 12
        entry.publish_day = 11
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertEqual(handler.convert_to_dict(entry), entry_dict)

    def test_get_entry_from_dict(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertIsInstance(handler.get_entry_from_dict(entry_dict), Entry)

    def test_option_date(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertRaises(RSSReaderException, lambda: handler.option_date("19950514", False, False, ""))

    def test_write_to_html_ind_err(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        entry = Entry()
        self.assertRaises(IndexError, lambda: handler.write_to_html(entry, ""))

    def test_write_to_html_rss_err(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        entry = Entry()
        self.assertRaises(RSSReaderException, lambda: handler.write_to_html(entry, " "))


if __name__ == '__main__':
    unittest.main()
