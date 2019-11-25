"""Module tests functions from process_func.py and print_func.py"""

import unittest
from unittest.mock import Mock
import feedparser
import argparse
import os

import functions.process_func as proc_f
import functions.print_func as print_f
import classes.exceptions as exc
from tests.test_caching import news_collection


class TestProcessFunctions(unittest.TestCase):
    """Class for testing process functions"""

    def setUp(self):
        # Get description root from local xml
        self.path_to_tests = os.path.abspath(os.path.dirname(__file__))
        self.feed = feedparser.parse(os.path.join(self.path_to_tests, "files/test_example.xml"))
        description = self.feed.entries[0].get("description", "")
        self.root = proc_f.get_xml_root(description)
        self.logger = Mock()


    def test_extract_text_from_description(self):
        """Tests function extract_text_from_description()"""
        # Assert description that was got by function and local file description
        with open(os.path.join(self.path_to_tests, "files/test_description.txt"), 'r') as text:
            local_file_description = text.read()
            self.assertEqual(proc_f.extract_text_from_description(self.root),
                            local_file_description)

    def test_extract_links_from_description(self):
        """Tests function extract_links_from_description()"""
        # Tuple of links
        links = (['http://rss.cnn.com/~ff/rss/cnn_topstories?a=0yorQIkIJGk:Sht6XkuB3rs:yIl2AUoC8zA',
                  'http://rss.cnn.com/~ff/rss/cnn_topstories?a=0yorQIkIJGk:Sht6XkuB3rs:7Q72WNTAKBA',
                  'http://rss.cnn.com/~ff/rss/cnn_topstories?a=0yorQIkIJGk:Sht6XkuB3rs:V_sGLiPBpWU',
                  'http://rss.cnn.com/~ff/rss/cnn_topstories?a=0yorQIkIJGk:Sht6XkuB3rs:qj6IDK7rITs',
                  'http://rss.cnn.com/~ff/rss/cnn_topstories?a=0yorQIkIJGk:Sht6XkuB3rs:gIN9vFwOqvQ'],
                 ['http://feeds.feedburner.com/~ff/rss/cnn_topstories?d=yIl2AUoC8zA',
                  'http://feeds.feedburner.com/~ff/rss/cnn_topstories?d=7Q72WNTAKBA',
                  'http://feeds.feedburner.com/~ff/rss/cnn_topstories?i=0yorQIkIJGk:Sht6XkuB3rs:V_sGLiPBpWU',
                  'http://feeds.feedburner.com/~ff/rss/cnn_topstories?d=qj6IDK7rITs',
                  'http://feeds.feedburner.com/~ff/rss/cnn_topstories?i=0yorQIkIJGk:Sht6XkuB3rs:gIN9vFwOqvQ',
                  'http://feeds.feedburner.com/~r/rss/cnn_topstories/~4/0yorQIkIJGk'])

        self.assertEqual(proc_f.extract_links_from_description(self.root), links)


    def test_parse_date(self):
        """Tests function parse_date"""
        date_str_from_func = proc_f.parse_date("20191122")
        self.assertEqual(date_str_from_func, "22 Nov 2019")

        with self.assertRaises(argparse.ArgumentTypeError):
            proc_f.parse_date("20191133")

        with self.assertRaises(argparse.ArgumentTypeError):
            proc_f.parse_date("201111bb")


    def test_process_feed(self):
        """Tests process_feed function"""
        command_line_args = Mock()
        command_line_args.source = "https://news.yahoo.com/rss/"
        news_collection = proc_f.process_feed(command_line_args, self.feed, self.logger)
        self.assertEqual(len(news_collection), 1)

        news = news_collection[0]
        self.assertEqual(news.command_line_args.source, "https://news.yahoo.com/rss/")
        date = "Thu, 31 Oct 2019 05:39:41 GMT"
        self.assertEqual(news.date, date)


class TestPrintFunctions(unittest.TestCase):

    def test_limit_news_collections(self):
        """Tests function limit_news_collections"""
        command_line_args = Mock()
        news_collection = [num for num in range(10)]
        logger = Mock()

        command_line_args.limit = -5
        with self.assertRaises(exc.LimitArgumentError):
            print_f.limit_news_collections(command_line_args, news_collection, logger)

        command_line_args.limit = 5
        self.assertEqual(len(print_f.limit_news_collections(command_line_args,
                                                  news_collection, logger)), 5)

        command_line_args.limit = 15
        self.assertEqual(len(print_f.limit_news_collections(command_line_args,
                                                  news_collection, logger)), 10)


    def test_generate_news_json(self):
        """Tests function generate news json"""
        logger = Mock()
        path_to_tests = os.path.abspath(os.path.dirname(__file__))
        js_from_func = print_f.generate_news_json(news_collection, logger)
        with open(os.path.join(path_to_tests, "files/json_example"), 'r') as file:
            js_from_file = file.read()
        self.assertEqual(js_from_func, js_from_file)


if __name__ == '__main__':
    unittest.main()
