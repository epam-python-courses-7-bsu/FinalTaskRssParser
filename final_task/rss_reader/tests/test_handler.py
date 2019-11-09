import os
import sys
import unittest
out_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(out_dir)
from Handler import Handler
from Entry import Entry


class TestEntry(unittest.TestCase):
    def test__init__(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertIsInstance(handler, Handler)
        self.assertNotIsInstance("handler", Handler)

    @unittest.skip("gen_entries() returns an object generator")
    def test_gen_entries(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertIsInstance(handler.gen_entries(), Entry)

    def test_convert_to_dict(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        entry = Entry("Title 1", "Wed, 06 Nov 2019 14:22:10 +0500", "https://link1.com", "description of article",
                      ["https://link1.com"]
                      )
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Links": ["https://link1.com"]
        }
        self.assertEqual(handler.convert_to_dict(entry), entry_dict)


if __name__ == '__main__':
    unittest.main()
