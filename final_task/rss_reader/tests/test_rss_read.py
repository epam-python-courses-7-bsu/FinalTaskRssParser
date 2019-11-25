import unittest
from Classes.rss_read import RSSParser


class RssRead(unittest.TestCase):
    def test_all_right(self):
        self.assertTrue(RSSParser("https://news.yahoo.com/rss/", 1, ['--colorize']))


if __name__ == '__main__':
    unittest.main()
