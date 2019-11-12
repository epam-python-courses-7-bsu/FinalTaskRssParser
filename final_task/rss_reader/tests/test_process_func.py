"""Module tests functions from process_func.py and print_func.py"""

import unittest
from unittest.mock import Mock
import functions.process_func as proc_f
from functions.print_func import check_limit_argument
import classes.exceptions as exc
import feedparser


class TestProcessFunctions(unittest.TestCase):
    """Class for testing process functions"""

    def setUp(self):
        # Get description root from local xml
        feed = feedparser.parse('files/test_example.xml')
        description = feed.entries[0].get("description", "")
        self.root = proc_f.get_xml_root(description)

    def test_extract_text_from_description(self):

        # Assert description that was got by function and local file description
        with open('files/test_description.txt', 'r') as text:
            local_file_description = text.read()
            self.assertEqual(proc_f.extract_text_from_description(self.root),
                             local_file_description)

    def test_extract_links_from_description(self):

        # Assert links that was got by function and local file links
        with open('files/test_links.txt', 'r') as text:
            local_file_links = text.read()
            self.assertEqual(proc_f.extract_links_from_description(self.root),
                             local_file_links)


class TestPrintFunctions(unittest.TestCase):
    """Class for testing output functions"""

    def test_check_limit_argument(self):
        # Mocking objects
        command_line_args = Mock()
        news_collection = [num for num in range(10)]
        logger = Mock()

        # Assert function check_limit_argument()
        # Limit is negative
        command_line_args.limit = -5
        with self.assertRaises(exc.LimitArgumentError):
            check_limit_argument(command_line_args, news_collection, logger)

        # Limit is positive and less than news_collection length
        command_line_args.limit = 5
        self.assertEqual(len(check_limit_argument(command_line_args,
                                                  news_collection, logger)), 5)

        # Limit is more than news_collection
        command_line_args.limit = 15
        self.assertEqual(len(check_limit_argument(command_line_args,
                                                  news_collection, logger)), 10)


if __name__ == '__main__':
    unittest.main()
