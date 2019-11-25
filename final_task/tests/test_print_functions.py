import sys
import os

sys.path.insert(1, 'final_task/rss_reader')
from parser_rss import *
from News import News

from io import StringIO
from unittest.mock import patch
import feedparser
import print_functions
import unittest


class TestPrintFunctios(unittest.TestCase):

    def setUp(self):
        self.item = News(feed="feed",
                         title="title",
                         date=parser.parse("2019-11-17 10:44:20-05:00"),
                         link="link",
                         info_about_image="info_about_image",
                         briefly_about_news="briefly_about_news",
                         links_from_news=["link", "link_on_image"]
                         )
        self.result = "1\n"
        self.result += "Feed: feed\n"
        self.result += "Title: title \n"
        self.result += "Date: 2019-11-17 10:44:20-05:00 \n"
        self.result += "Link: link\n"
        self.result += "Info about image: info_about_image\n"
        self.result += "Briefly about news: briefly_about_news\n"
        self.result += "Links: \n"
        self.result += "[0] link\n"
        self.result += "[1] link_on_image\n"
        self.result += '\n'
        self.result += '-' * 100

        if os.path.isfile('final_task/tests/news_feed_for_test.xml'):
            self.url = 'final_task/tests/news_feed_for_test.xml'
        else:
            self.url = 'news_feed_for_test.xml'

        self.news_feed = feedparser.parse(self.url)

    def test_print_news(self):
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            print_functions.print_news([self.item, ])
            self.assertEqual(fake_out_put.getvalue().strip(), self.result)

    def test_print_news_in_json(self):
        self.result = "[\n"
        self.result += "    {\n"
        self.result += '''        "Feed": "feed",\n'''
        self.result += '''        "Title": "title",\n'''
        self.result += '''        "Date": "2019-11-17 10:44:20-05:00",\n'''
        self.result += '''        "Link": "link",\n'''
        self.result += '''        "Info about image": "info_about_image",\n'''
        self.result += '''        "Briefly about news": "briefly_about_news",\n'''
        self.result += '''        "Links": [\n'''
        self.result += '''            "link",\n'''
        self.result += '''            "link_on_image"\n'''
        self.result += "        ]\n"
        self.result += "    }\n"
        self.result += "]"
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            print_functions.print_news_in_json([self.item, ])
            self.assertEqual(fake_out_put.getvalue().strip(), self.result)

    def test_print_news_in_json_in_multi_colored_format(self):
        self.result = "\033[1m\033[35m[\033[0m\n"
        self.result += "    \033[1m\033[31m{\033[0m\n"
        self.result += '''        \033[1m\033[34m"Feed": "feed",\033[0m\n'''
        self.result += '''        \033[32m"Title": "title",\033[0m\n'''
        self.result += '''        \033[33m"Date": "2019-11-17 10:44:20-05:00",\033[0m\n'''
        self.result += '''        \033[36m"Link": "link",\033[0m\n'''
        self.result += '''        \033[33m"Info about image": "info_about_image",\033[0m\n'''
        self.result += '''        \033[32m"Briefly about news": "briefly_about_news",\033[0m\n'''
        self.result += '''        \033[36m"Links": [\n'''
        self.result += '''            "link",\n'''
        self.result += '''            "link_on_image"\n'''
        self.result += "        ]\033[0m\n"
        self.result += "    \033[1m\033[31m}\033[0m\n"
        self.result += "\033[1m\033[35m]\033[0m"
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            print_functions.print_news_in_json_in_multi_colored_format([self.item, ])
            self.assertEqual(fake_out_put.getvalue().strip(), self.result)

    def test_print_news_in_multi_colored_format(self):
        self.result = "1:\n"
        self.result += "Feed: feed\n"
        self.result += "Title: title\n"
        self.result += "Date: 2019-11-17 10:44:20-05:00\n"
        self.result += "Link: link\n"
        self.result += "Info about image: info_about_image\n"
        self.result += "Briefly about news: briefly_about_news\n"
        self.result += "Links: \n"
        self.result += "[0] link\n"
        self.result += "[1] link_on_image"
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            print_functions.print_news_in_multi_colored_format([self.item, ])
            self.assertEqual(fake_out_put.getvalue().strip(), self.result)


if __name__ == '__main__':
    unittest.main()
