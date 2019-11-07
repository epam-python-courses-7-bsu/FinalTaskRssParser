"""This module tests rss_parser module
"""

import unittest
import rss_parser


class RSSParser(unittest.TestCase):
    def test_get_rss(self):
        self.assertEqual(rss_parser.get_rss('https://www.google.com'), None)
        self.assertNotEqual(rss_parser.get_rss('https://news.yahoo.com/rss/'), None)

    def test_connect_url(self):
        self.assertEqual(rss_parser.connect_rss('https://httpstat.us/200'), True)
        self.assertEqual(rss_parser.connect_rss('https://httpstat.us/504'), False)
        self.assertEqual(rss_parser.connect_rss('https://httpstat.us/405'), False)
        self.assertEqual(rss_parser.connect_rss('https://httpstat.us/511'), False)


if __name__ == '__main__':
    unittest.main()





