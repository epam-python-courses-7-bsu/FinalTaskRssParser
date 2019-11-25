""" Testing module for caching functions. """
import unittest
from unittest import mock

import os
from models import NewsEntry
import caching_functions as cache_func
import exceptions as exc

"""Create news instances"""
title = "Stars Are Being Born in the Depths of a Black Hole"
date = "Tue, 19 Nov 2019 15:47 EST"
link = "http://www.nasa.gov/image-feature/stars-are-being-born-in-the-depths-of-a-black-hole"
summary = """ In the Phoenix Constellation, astronomers have confirmed the first example 
       of a galaxy cluster where large numbers of stars are being born at its core. """
feed_title = "NASA Image of the Day"
feed_language = "en-us"
source = "file:///tmp/mozilla_anna0/lg_image_of_the_day.rss"

news1 = NewsEntry(feed_title, feed_language, title, summary, date, link, source)

title = "Stars Are Being Born in the Depths of a Black Hole - 2"
date = "Tue, 19 Nov 2018 15:47 EST"
link = "http://www.nasa./new/gov/image-feature/stars-are-being-born-in-the-depths-of-a-black-hole"
summary = """ In the Phoenix Constellation, astronomers have confirmed the first example 
       of a galaxy cluster where large numbers of stars are being born at its core. """
feed_title = "NASA Image of the Day"
feed_language = "en-us"
source = "file:///tmp/mozilla_anna0/lg_image_of_the_day.rss"
image_links = ["link1, link2"]
news2 = NewsEntry(feed_title, feed_language, title, summary, date, link, source, image_links)

news_collection = [news1, news2]

DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class TestCachingFunctions(unittest.TestCase):
    def setUp(self):
        """Initialize collections of news"""
        self.news1 = news1
        self.news2 = news2
        self.news_collection = news_collection
        self.logger = mock.Mock()
        self.command_line_args = mock.Mock()

        self.home_dir = os.path.expanduser('~')
        self.test_file_path = os.path.join(DIRECTORY, '.test_cache_rss_news')
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @mock.patch("os.path.join")
    def test_cache_news_and_get_cache_news(self, path):
        path.return_value = self.test_file_path
        cache_func.cache_news(self.news_collection, self.logger)

        self.command_line_args.limit = 3
        self.command_line_args.date = "11 Nov 2018"
        self.command_line_args.source = ''
        with self.assertRaises(exc.EmptyCollectionError):
            cache_func.get_cached_news(self.command_line_args, self.logger)

        self.command_line_args.date = "19 Nov 2019"
        self.command_line_args.source = 'Source'
        with self.assertRaises(exc.EmptyCollectionError):
            cache_func.get_cached_news(self.command_line_args, self.logger)

        self.command_line_args.date = "19 Nov 2019"
        self.command_line_args.source = ''
        get_news_collection = cache_func. \
            get_cached_news(self.command_line_args, self.logger)
        num_of_news = len(get_news_collection)
        self.assertEqual(num_of_news, 1)

        self.command_line_args.date = "19 Nov 2019"
        self.command_line_args.source =\
            "file:///tmp/mozilla_anna0/lg_image_of_the_day.rss"
        get_news_collection = cache_func.get_cached_news(self.command_line_args, self.logger)
        num_of_news = len(get_news_collection)
        self.assertEqual(num_of_news, 1)
        news_title = "Stars Are Being Born in the Depths of a Black Hole"
        self.assertEqual(news_collection[0].title, news_title)


if __name__ == '__main__':
    unittest.main()
