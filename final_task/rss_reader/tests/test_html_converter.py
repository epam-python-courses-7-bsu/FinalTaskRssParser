#!/usr/bin/env python3.8
"""Module for testing html_converter.py"""

import unittest
from unittest.mock import Mock

import dominate

import html_converter as conv


class TestCheckFunctions(unittest.TestCase):
    """
    Tests functions from html_converter.py
    """

    def setUp(self):
        self.all_news = [
            {'feed_title': 'Yahoo News - Latest News & Headlines',
             'feed_url': 'https://news.yahoo.com/rss/',
             'title': '4 reasons Democrats have an uphill climb on Donald Trump impeachment and removal',
             'link': 'https://news.yahoo.com/4-reasons-democrats-uphill-climb-100009122.html',
             'date': 'Fri, 22 Nov 2019 05:00:09 -0500',
             'img_title':
                 ['4 reasons Democrats have an uphill climb on Donald Trump impeachment and removal'],
             'img_link':
                 ['http://l1.yimg.com/uu/api/res/1.2/o5MXQ3QgenGRlHhxIdEvWg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs'
                  '-/https://media.zenfs.com/en-us/usa_today_opinion_532/e76829b608aaa4e825a37860afc0e4aa'],
             'text': 'If the ending of this movie is inevitable, the undecided public may move toward the '
                     'Republican claim that the whole thing is a waste of time and money.'}
        ]

        self.cmd_args = Mock()
        self.cmd_args.date = ''
        self.rss_html_doc = dominate.document(title='RSS News')

    def test_convert_new_in_html(self):
        """
        Test convert_new_in_html(cmd_args, all_news, rss_html_doc, logger)
        """
        html_from_func = conv.convert_new_in_html(self.cmd_args, self.all_news[0], self.rss_html_doc)
        with open("tests/files/example_html.html", "r") as file:
            html_draft = file.read()
            self.assertEqual(str(html_from_func), html_draft)


if __name__ == '__main__':
    unittest.main()
