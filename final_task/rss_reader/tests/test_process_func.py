"""Module tests functions from process_func.py and print_func.py"""

import unittest
from unittest.mock import Mock
import functions.process_func as proc_f
from functions.print_func import limit_news_collections
import classes.exceptions as exc
import feedparser


class TestProcessFunctions(unittest.TestCase):
    """Class for testing process functions"""

    def setUp(self):
        # Get description root from local xml
        feed = feedparser.parse('tests/files/test_example.xml')
        description = feed.entries[0].get("description", "")
        self.root = proc_f.get_xml_root(description)


    def test_extract_text_from_description(self):
        """Tests function extract_text_from_description()"""
        # Assert description that was got by function and local file description
        with open('tests/files/test_description.txt', 'r') as text:
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


class TestPrintFunctions(unittest.TestCase):
    """Class for testing output functions"""

    def test_limit_news_collections(self):
        """Test function limit_news_collections"""
        # Mocking objects
        command_line_args = Mock()
        news_collection = [num for num in range(10)]
        logger = Mock()

        # Assert function check_limit_argument()
        # Limit is negative
        command_line_args.limit = -5
        with self.assertRaises(exc.LimitArgumentError):
            limit_news_collections(command_line_args, news_collection, logger)

        # Limit is positive and less than news_collection length
        command_line_args.limit = 5
        self.assertEqual(len(limit_news_collections(command_line_args,
                                                  news_collection, logger)), 5)

        # Limit is more than news_collection
        command_line_args.limit = 15
        self.assertEqual(len(limit_news_collections(command_line_args,
                                                  news_collection, logger)), 10)


if __name__ == '__main__':
    unittest.main()
