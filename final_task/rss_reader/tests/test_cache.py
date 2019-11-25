#!/usr/bin/env python3.8
"""Module for testing cache.py"""

import os
import unittest
from unittest.mock import patch, Mock

import cache
import rss_exceptions as ex


class TestCheckFunctions(unittest.TestCase):
    """
    Tests functions from cache.py
    """

    def setUp(self):
        self.logger = Mock()
        self.cmd_args = Mock()
        self.limit = Mock()
        self.parsed_news = [
            {'feed_title': 'Yahoo News - Latest News & Headlines',
             'feed_url': 'https://news.yahoo.com/rss/',
             'title': 'First news name',
             'link': 'Link № 1.1',
             'date': 'Fri, 22 Nov 2019 10:36:29 -0500',
             'img_title': ['Title for image № 1'],
             'img_link': ['Link № 1.2'],
             'text': 'some text № 1'},
            {'feed_title': 'Yahoo News - Latest News & Headlines',
             'feed_url': 'https://news.yahoo.com/rss/',
             'title': 'Second news name',
             'link': 'Link № 2.1',
             'date': 'Fri, 21 Nov 2019 21:36:29 -0500',
             'img_title': ['Title for image № 2'],
             'img_link': ['Link № 2.2'],
             'text': 'some text № 2'}
        ]
        self.directory = os.path.abspath(os.path.dirname(__file__))
        self.test_db_path = os.path.join(self.directory, '.test_cache')

        # remove '.test_cache', if exists, before testing cache.py
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_get_cached_news(self):
        """
        Test get_cached_news(cmd_args, logger)
        """
        with patch("os.path.join", return_value=os.path.join(self.test_db_path)):
            # If storage doesn't exists raise an exception
            with self.assertRaises(ex.EmptyCacheError):
                cache.get_cached_news(self.cmd_args)

            # Create storage
            cache.cache_news(self.parsed_news)

            self.cmd_args.date = "21 Nov 2019"
            self.cmd_args.limit = 10
            self.cmd_args.source = 'https://news.yahoo.com/rss/'
            list_of_extracted_new = cache.get_cached_news(self.cmd_args)
            length_new_collection = len(list_of_extracted_new)
            self.assertEqual(length_new_collection, 1)

            self.cmd_args.date = "22 Nov 2019"
            self.cmd_args.limit = 10
            self.cmd_args.source = 'wrong_url'
            with self.assertRaises(ex.SpecifiedDayNewsError):
                cache.get_cached_news(self.cmd_args)

            self.cmd_args.date = "23 Nov 2019"
            self.cmd_args.limit = 10
            self.cmd_args.source = ''
            with self.assertRaises(ex.SpecifiedDayNewsError):
                cache.get_cached_news(self.cmd_args)

            self.cmd_args.date = "21 Nov 2019"
            self.cmd_args.limit = 0
            self.cmd_args.source = ''
            list_of_extracted_new = cache.get_cached_news(self.cmd_args)
            length_new_collection = len(list_of_extracted_new)
            self.assertEqual(length_new_collection, 1)


if __name__ == '__main__':
    unittest.main()
