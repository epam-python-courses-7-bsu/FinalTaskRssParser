"""Module for testing of functions from convertation.py"""
import unittest
from unittest.mock import Mock
import dominate
import os

import functions.convertation as conv
from tests.test_caching import news1


class TestConvertationFunctions(unittest.TestCase):

    def setUp(self):
        """Initialize News instance"""
        self.news1 = news1
        self.path_to_tests = os.path.abspath(os.path.dirname(__file__))
        self.internet = Mock(return_value=False)
        self.doc_html = dominate.document(title='RSS News')


    def test_create_html_news_entry(self):
        """Tests html news entry creation"""
        html_from_func = conv.create_html_news_entry(self.news1, self.doc_html, self.internet)
        with open(os.path.join(self.path_to_tests, "files/entry.html"), "r") as file:
            html_entry = file.read()
            self.assertEqual(str(html_from_func), html_entry)


    def test_create_html_news_entry_for_epub(self):
        """Tests html news entry creation for epub"""
        image_number = 1
        list_of_image_objects, image_number = conv.create_image_objects(self.news1, image_number)
        html_from_func = conv.create_html_news_entry_for_epub(self.news1,
                                                              self.doc_html,
                                                              self.internet,
                                                              list_of_image_objects)
        with open(os.path.join(self.path_to_tests, "files/epub_entry.html"), "r") as file:
            html_entry = file.read()
            self.assertEqual(str(html_from_func), html_entry)


if __name__ == '__main__':
    unittest.main()