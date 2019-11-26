#!/usr/bin/env python3.8
"""Module for testing rss_parser.py"""

import os
import unittest
from unittest.mock import Mock

from rss_parser import RSSparser


class TestRSSparser(unittest.TestCase):
    """
    Tests functions from cmd_line_parser.py
    """

    def setUp(self):
        self.cmd_args = Mock()
        directory = os.path.abspath(os.path.dirname(__file__))
        test_db_path = os.path.join(directory, 'files/rss_xml_template.xml')
        self.cmd_args.source = test_db_path
        self.cmd_args.limit = 100

    def test_rss_parser(self):
        """
        Test class RSSparser(self.cmd_args)
        """
        parser = RSSparser(self.cmd_args)
        all_news = parser.parse_feed()
        all_news_length = len(all_news)
        self.assertEqual(all_news_length, 5)

        first_news = all_news[0]
        title = 'Mars Science Lab launch delayed two years'
        self.assertEqual(first_news['title'], title)


if __name__ == '__main__':
    unittest.main()
