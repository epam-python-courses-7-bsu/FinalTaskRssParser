"""Module for testing caching functions and News class methods"""
import unittest
import os
from unittest.mock import Mock, patch

from functions.caching import cache_news, get_cached_news
from classes.news_class import News
from classes.exceptions import ExtractNewsException


"""Create news instances"""
title = "UN warns Bolivia crisis could ‘spin out of control’ after nine killed in latest violence"
date = "Sun, 17 Nov 2019 10:49:00 -0500"
link = "https://news.yahoo.com/un-warns-boliva-crisis-could-154900324.html"
text = """
       The United Nations has warned mounting unrest in Bolivia could “spin out of control”
       after nine people died in the latest escalation of violence between between security
       forces and supporters of former president Evo Morales.
       """
links = (['https://news.yahoo.com/utah.html'],
         ['http://l2.yimg.com/uu/'])
feed_title = "Yahoo News - Latest News & Headlines"
source = "https://news.yahoo.com/rss/"

news1 = News(title, date, link, text, links, feed_title, source)

title = "Japan space probe on its way back after asteroid mission"
date = "Mon, 17 Nov 2019 05:29:05 -0500"
link = """Link"""
text = """A Japanese space probe is heading home from an asteroid 250 million km"""
links = (
    [
        'https://news.yahoo.com/bolivian-government.html',
        'http://l2.yimg.com/uu/api/res/1.2/zxoWO_y.zm2ZkQv',
        'http://l2.yimg.com/uu/api/res/1.2/U9sExM03VAtbtwl0NbAOxg'
    ],
    [
        'https://news.yahoo.com/showdown-looms-over-syri.html',
        'http://l1.yimg.com/uu/api/res/1.2/Zgv4MFMRzaa',
        'http://l.yimg.com/uu/api/res/1.2/Br3NUzkxWrDTnUtc5.E',
    ]
)
feed_title = "Reuters: Science News"
source = "http://feeds.reuters.com/reuters/scienceNews"
news2 = News(title, date, link, text, links, feed_title, source, )

news_collection = [news1, news2]


class TestCachingFunctions(unittest.TestCase):
    """Tests functions from caching.py"""

    def setUp(self):
        """Initialize collections of news"""
        self.news1 = news1
        self.news2 = news2
        self.news_collection = news_collection
        self.logger = Mock()
        self.command_line_args = Mock()

        # Clear test database
        self.home_dir = os.path.expanduser('~')
        self.database_path = os.path.join(self.home_dir, 'test_feed')
        if os.path.exists(self.database_path):
            os.remove(self.database_path)



    def test_func_cache_news_and_get_news(self):
        """Tests cache_news() and get_news()"""
        with patch("os.path.join", return_value=os.path.join(self.database_path)):
            cache_news(self.news_collection, self.logger)

            self.command_line_args.date = "18 Nov 2019"
            self.command_line_args.source = ''
            with self.assertRaises(ExtractNewsException):
                get_cached_news(self.command_line_args, self.logger)

            self.command_line_args.date = "17 Nov 2019"
            self.command_line_args.source = ''
            news_collection = get_cached_news(self.command_line_args, self.logger)
            length_of_news = len(news_collection)
            self.assertEqual(length_of_news, 2)

            self.command_line_args.date = "17 Nov 2019"
            self.command_line_args.source = "https://news.yahoo.com/rss/"
            news_collection = get_cached_news(self.command_line_args, self.logger)
            length_of_news = len(news_collection)
            self.assertEqual(length_of_news, 1)
            news_from_func = news_collection[0]
            title = "UN warns Bolivia crisis could ‘spin out of control’ after nine killed in latest violence"
            self.assertEqual(news_from_func.title, title)


    def test_news_class_methods(self):
        """Tests methods of news class"""

        string_of_links = """[1] https://news.yahoo.com/utah.html\n[2] http://l2.yimg.com/uu/\n"""
        list_of_links = ['https://news.yahoo.com/utah.html', 'http://l2.yimg.com/uu/']

        self.assertEqual(self.news1.create_list_of_links(), list_of_links)
        self.assertEqual(self.news1.create_string_of_links(), string_of_links)



if __name__ == '__main__':
    unittest.main()
