"""Module for testing of functions from convertation.py"""
import unittest
from unittest.mock import Mock
import functions.convertation as conv
import dominate
from classes.news_class import News


class TestConvertationFunctions(unittest.TestCase):

    def setUp(self):
        """Initialize News instance"""
        title = "UN warns Bolivia crisis could ‘spin out of control’ after nine killed in latest violence"
        date = "Sun, 17 Nov 2019 10:49:00 -0500"
        link = "https://news.yahoo.com/un-warns-boliva-crisis-could-154900324.html"
        text = """
               The United Nations has warned mounting unrest in Bolivia could “spin out of control” after nine people died in
               the latest escalation of violence between between security forces and supporters of former president Evo Morales.Protesters
               loyal to Mr Morales, who resigned from office and fled to Mexico after being accused of electoral fraud, were fired upon by
               armed police on Friday after attempting to cross a military checkpoint in the central city of Sacaba.
               """
        links = (
                ['https://news.yahoo.com/un-warns-boliva-crisis-could-154900324.html'],
                ['http://l.yimg.com/uu/api/res/1.2/SzofFuNzc8PeuqYDqsjYCg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/the_independent_635/62d924d34aaee1219a1502a5d2387cc1']
                )
        feed_title = "Yahoo News - Latest News & Headlines"
        source = "https://news.yahoo.com/rss/"
        command_line_args = Mock()
        self.news1 = News(title, date, link, text, links, feed_title, source, command_line_args)

        self.internet = Mock(return_value=False)
        self.doc_html = dominate.document(title='RSS News')


    def test_create_html_news_entry(self):
        """Tests html news entry creation"""

        html_from_func = conv.create_html_news_entry(self.news1, self.doc_html, self.internet)
        with open("tests/files/entry.html", "r") as file:
            html_entry = file.read()
            self.assertEqual(str(html_from_func), html_entry)


    def test_create_html_news_entry_for_epub(self):
        """Tests html news entry creation for epub"""
        image_number = 1
        list_of_image_objects, image_number = conv.create_image_objects(self.news1, image_number)
        html_from_func = conv.create_html_news_entry_for_epub(self.news1, self.doc_html, self.internet, list_of_image_objects)
        with open("tests/files/epub_entry.html", "r") as file:
            html_entry = file.read()
            self.assertEqual(str(html_from_func), html_entry)


if __name__ == '__main__':
    unittest.main()