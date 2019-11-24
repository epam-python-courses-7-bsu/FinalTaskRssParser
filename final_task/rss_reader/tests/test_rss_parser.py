"""This module tests rss_parser module
"""
import re
import os
import sys

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

DIR = 'tests'

THIS_DIRECTORY = re.sub(DIR, '', THIS_DIRECTORY)

sys.path.append(THIS_DIRECTORY)


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

    def test_convert_date(self):
        self.assertEqual(rss_parser.convert_date('Fri, 22 Nov 2019 15:47:25 -0500'), '20191122')
        self.assertNotEqual(rss_parser.convert_date('Fri, 22 Nov 2019 15:47:25 -0500'), '20192211')
        self.assertEqual(rss_parser.convert_date('Sat, 23 Nov 2019 18:50:07 -0500'), '20191123')
        self.assertNotEqual(rss_parser.convert_date('Sat, 23 Nov 2019 18:50:07 -0500'), '20192311')


if __name__ == '__main__':
    unittest.main()





