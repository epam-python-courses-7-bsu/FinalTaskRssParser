"""Module for testing caching functions and News class methods"""
import unittest
import os
from unittest.mock import Mock, patch

from functions.caching import cache_news, get_cached_news
from classes.news_class import News
from classes.exceptions import ExtractNewsException


class TestCachingFunctions(unittest.TestCase):
    """Tests functions from caching.py"""

    def setUp(self):
        """Initialize collections of news"""
        self.command_line_args = "command line args"
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
        self.news1 = News(title, date, link, text, links, feed_title, source, self.command_line_args)

        title = "Japan space probe on its way back after asteroid mission"
        date = "Mon, 17 Nov 2019 05:29:05 -0500"
        link = """
               http://feeds.reuters.com/~r/reuters/scienceNews/~3/kCJoocMNmuY/japan-space-probe-on-its
               -way-back-after-asteroid-mission-idUSKBN1XS13P
               """
        text = """
               A Japanese space probe is heading home from an asteroid 250 million km (155 million miles) from Earth after collecting
               sub-surface samples that could help scientists seeking the origins of life, Japan's space agency said on Monday.
               """
        links = (
                [
                'http://feeds.reuters.com/~ff/reuters/scienceNews?a=kCJoocMNmuY:JksatCm2x24:yIl2AUoC8zA',
                'http://feeds.reuters.com/~ff/reuters/scienceNews?a=kCJoocMNmuY:JksatCm2x24:F7zBnMyn0Lo',
                'http://feeds.reuters.com/~ff/reuters/scienceNews?a=kCJoocMNmuY:JksatCm2x24:V_sGLiPBpWU'
                ],
                [
                'http://feeds.feedburner.com/~ff/reuters/scienceNews?d=yIl2AUoC8zA',
                'http://feeds.feedburner.com/~ff/reuters/scienceNews?i=kCJoocMNmuY:JksatCm2x24:F7zBnMyn0Lo',
                'http://feeds.feedburner.com/~ff/reuters/scienceNews?i=kCJoocMNmuY:JksatCm2x24:V_sGLiPBpWU',
                'http://feeds.feedburner.com/~r/reuters/scienceNews/~4/kCJoocMNmuY'
                ]
                )
        feed_title = "Reuters: Science News"
        source = "http://feeds.reuters.com/reuters/scienceNews"
        self.news2 = News(title, date, link, text, links, feed_title, source, self.command_line_args)

        self.news_collection = [self.news1, self.news2]
        self.logger = Mock()


        # Clear test database
        self.home_dir = os.path.expanduser('~')
        self.database_path = os.path.join(self.home_dir, 'test_feed')
        if os.path.exists(self.database_path):
            os.remove(self.database_path)



    def test_func_cache_news_and_get_news(self):
        """Tests cache_news() and get_news()"""

        with patch("os.path.join", return_value=os.path.join(self.database_path)):
            cache_news(self.news_collection, self.logger)
            self.command_line_args = Mock()
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
            got_news = news_collection[0]
            title = "UN warns Bolivia crisis could ‘spin out of control’ after nine killed in latest violence"
            self.assertEqual(got_news.title, title)


    def test_news_class_methods(self):
        """Tests methods of news class"""

        string_of_links = """[1] https://news.yahoo.com/un-warns-boliva-crisis-could-154900324.html
[2] http://l.yimg.com/uu/api/res/1.2/SzofFuNzc8PeuqYDqsjYCg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/the_independent_635/62d924d34aaee1219a1502a5d2387cc1
"""
        list_of_links = ['https://news.yahoo.com/un-warns-boliva-crisis-could-154900324.html',
                         'http://l.yimg.com/uu/api/res/1.2/SzofFuNzc8PeuqYDqsjYCg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/the_independent_635/62d924d34aaee1219a1502a5d2387cc1']

        self.assertEqual(self.news1.create_list_of_links(), list_of_links)
        self.assertEqual(self.news1.create_string_of_links(), string_of_links)



if __name__ == '__main__':
    unittest.main()
