import os
import sys
import json
import unittest
from unittest.mock import patch, call

sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + '/rss_reader'))  # noqa #402

from exceptions import WrongResponseTypeError
from rss_reader import go_for_rss, check_response, output_format, print_result
from news_articles import NewsArticle


class TestRssReader(unittest.TestCase):

    def setUp(self):
        self.headers = {'Content-Type': ''}
        self.news_article_1 = NewsArticle(news_outlett_name='Yahoo News',
                                          news_title='OK Boomer',
                                          pub_date='Fri, 22 Nov 2019 15:47:25 -0500',
                                          news_link='news link',
                                          news_description='A long news description',
                                          img_alt='Smile sunshine',
                                          img_src='IMG link')

    def test_go_for_rss(self):
        with patch('rss_reader.request.urlopen') as mocked_urlopen:
            go_for_rss('https://news.yahoo.com/rss/')
            assert mocked_urlopen.mock_calls == [call('https://news.yahoo.com/rss/')]

    def test_check_response(self):
        content_types = ["application/xml", "application/rss+xml", "text/xml"]
        for type_ in content_types:
            self.headers['Content-Type'] = type_
            self.assertEqual(check_response(self), self)
        self.headers['Content-Type'] = 'AbraCadabra'
        self.assertRaises(WrongResponseTypeError, check_response, self)
        self.headers['Content-Type'] = ''
        self.assertRaises(WrongResponseTypeError, check_response, self)

    def test_output_format(self):
        output_format_result = list(output_format([self.news_article_1], True))
        self.assertEqual(output_format_result[0],
                         json.dumps(self.news_article_1.__dict__, ensure_ascii=False, indent=4))
        output_format_result = list(output_format([self.news_article_1], False))
        self.assertEqual(output_format_result[0], self.news_article_1)

    def test_print_result(self):
        with patch('builtins.print') as mocked_print:
            print_result([self.news_article_1, self.news_article_1], 2)
            assert mocked_print.mock_calls == [call(self.news_article_1), call(self.news_article_1)]
            mocked_print.mock_calls = []
            print_result([self.news_article_1, self.news_article_1], 1)
            assert mocked_print.mock_calls == [call(self.news_article_1)]


if __name__ == "__main__":
    unittest.main()
