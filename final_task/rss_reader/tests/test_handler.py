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

    def setUp(self):
        self.handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)

    def test_convert_to_dict(self):
        entry = Entry("Yahoo News - Latest News & Headlines", "Title 1", "Wed, 06 Nov 2019 14:22:10 +0500",
                      "https://link1.com", "summary", ("https://link1.com",))
        entry.publish_year = 2019
        entry.publish_month = 12
        entry.publish_day = 11
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertEqual(self.handler.convert_Entry_to_dict(entry), entry_dict)

    def test_convert_to_dict_fail(self):
        entry = Entry("Yahoo News - Latest News & Headlines", "Title 15", "Wed, 06 Nov 2019 14:22:10 +0500",
                      "https://link1.com", "summary", ("https://link1.com",))
        entry.publish_year = 2019
        entry.publish_month = 12
        entry.publish_day = 11
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertNotEqual(self.handler.convert_Entry_to_dict(entry), entry_dict)

    def test_get_entry_from_dict_instance(self):
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertIsInstance(self.handler.get_entry_from_dict(entry_dict), Entry)

    def test_get_entry_from_dict_not_instance(self):
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertNotIsInstance(self.handler.get_entry_from_dict(entry_dict), Handler)

    def test_option_date(self):
        self.assertRaises(RSSReaderException, lambda: self.handler.option_date("19950514", False, False, ""))


if __name__ == '__main__':
    unittest.main()
