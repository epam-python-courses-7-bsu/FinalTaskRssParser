"""Module tests functions from process_func.py and print_func.py
Tested functions:
-----------------
    extract_text_from_description(root)
    extract_links_from_description(root)
    check_limit_argument(command_line_args, news_collection, logger)

Depend on local files:
----------------------
    RSS_reader/files/test_example.xml
    RSS_reader/files/test_description.txt
    RSS_reader/files/test_links.txt
"""

import unittest
from unittest.mock import Mock
import functions.process_func as proc_f
import functions.check_func as ch_f
import functions.print_func as print_f
import builtins


class TestProcessFunctions(unittest.TestCase):
    """Class for testing process functions"""

    def setUp(self):
        # Mocking passed arguments
        command_line_args = Mock()
        command_line_args.source = 'files/test_example.xml'
        logger = Mock()

        # Mocking function check_feed_status()
        def side_effect(arg1, arg2):
            return arg1
        ch_f.check_feed_status = Mock(side_effect=side_effect)

        # Get description root from local xml file
        feed = proc_f.parse_feed(command_line_args, logger)
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
        builtins.input = Mock(return_value=8)

        # Assert function check_limit_argument()
        # Limit is negative
        command_line_args.limit = -5
        self.assertEqual(len(print_f.check_limit_argument(command_line_args,
                                                          news_collection, logger)), 8)

        # Limit is positive and less than news_collection length
        command_line_args.limit = 5
        self.assertEqual(len(print_f.check_limit_argument(command_line_args,
                                                          news_collection, logger)), 5)

        # Limit is more than news_collection
        command_line_args.limit = 15
        self.assertEqual(len(print_f.check_limit_argument(command_line_args,
                                                          news_collection, logger)), 10)


if __name__ == '__main__':
    unittest.main()
