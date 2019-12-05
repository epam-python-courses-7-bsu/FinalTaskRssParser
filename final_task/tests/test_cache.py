import os
import sys
import unittest
from unittest.mock import patch, call

sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + '/rss_reader'))  # noqa #402

from exceptions import CacheNotFoundError
from news_articles import NewsArticle
from cache import format_cache, update_cache, read_from_file, read_cache, write_to_file, save_cache


class TestCache(unittest.TestCase):

    def setUp(self):
        self.news_article_1 = NewsArticle(news_outlett_name='Yahoo News',
                                          news_title='OK Boomer',
                                          pub_date='Fri, 22 Nov 2019 15:47:25 -0500',
                                          news_link='news link',
                                          news_description='A long news description',
                                          img_alt='Smile sunshine',
                                          img_src='IMG link')
        self.news_article_2 = NewsArticle(news_outlett_name='Yahoo',
                                          news_title='Boomer',
                                          pub_date='Fri, 22 Nov 2019 15:47:25 -0500',
                                          news_link='link',
                                          news_description='A description',
                                          img_alt='Smile',
                                          img_src='IMG link')

        self.url = 'https://news.yahoo.com/rss/'
        self.another_url = 'https://another.url.com/rss/'
        self.date = '20191122'
        self.cache = {self.date: {self.url: {self.news_article_1}}}

    def test_format_cache(self):
        # on creation
        self.assertEqual(format_cache([self.news_article_1], self.url), self.cache)
        # with the same date
        news_articles = [self.news_article_1, self.news_article_2]
        self.assertEqual(format_cache(news_articles, self.url),
                         {self.date: {self.url: {self.news_article_1, self.news_article_2}}})
        # with diffrent dates
        self.news_article_2.pub_date = 'Fri, 25 Nov 2019 15:47:25 -0500'
        self.assertEqual(format_cache(news_articles, self.url),
                         {**self.cache, **{'20191125': {self.url: {self.news_article_2}}}})

    def test_update_cache(self):
        cache_same_url = {self.url: {self.news_article_2}}
        cache_another_url = {self.another_url: {self.news_article_2}}

        # stored cache with the same url
        self.assertEqual(update_cache(cache_same_url, self.cache, self.date, self.url),
                         {self.url: {self.news_article_1, self.news_article_2}})
        # stored cache with a diffrent url
        self.assertEqual(update_cache(cache_another_url, self.cache, self.date, self.url),
                         {**self.cache[self.date], **{self.another_url: {self.news_article_2}}})
        # without stored cache
        self.assertEqual(update_cache(None, self.cache, self.date, self.url), {**self.cache[self.date]})

    def test_read_cache(self):
        with patch('cache.read_from_file') as mocked_read:
            # [0] one elem in cache, [1] few elements with different urls
            test_cases = [self.cache[self.date], {self.url: {self.news_article_1, self.news_article_2},
                                                  self.another_url: {self.news_article_2}}]
            for cache in test_cases:
                mocked_read.return_value = cache
                read_cache(self.date, self.url, limit=100)
                read_cache(self.date, 'ALL', limit=100)
            # if provided wrong source
            self.assertRaises(CacheNotFoundError, read_cache, self.date, 'wrong source', limit=100)
            # if no elem in cache
            mocked_read.return_value = None
            self.assertRaises(CacheNotFoundError, read_cache, self.date, 'ALL', limit=100)

    def test_read_from_file(self):
        test_file_path = f'/tmp/rss_reader/cache/{self.date}.cache'
        with patch('builtins.open') as file_mock:
            with patch('pickle.load') as mocked_load:
                read_from_file(self.date)
                file_mock.assert_called_with(test_file_path, 'rb')
                mocked_load.assert_called_with(file_mock().__enter__())

    def test_write_to_file(self):
        test_file_path = f'/tmp/rss_reader/cache/{self.date}.cache'
        with patch('builtins.open') as file_mock:
            with patch('pickle.dump') as mocked_dump:
                write_to_file(self.cache, self.date)
                file_mock.assert_called_with(test_file_path, 'wb')
                mocked_dump.assert_called_with(self.cache, file_mock().__enter__(), protocol=None)

    def test_save_cache(self):
        self.news_article_2.pub_date = 'Fri, 23 Nov 2019 15:47:25 -0500'
        news_articles = [self.news_article_1, self.news_article_2]
        with patch('cache.read_from_file') as mocked_read:
            save_cache(news_articles, self.url)
            assert call('20191122') and call('20191123') in mocked_read.mock_calls


if __name__ == "__main__":
    unittest.main()
