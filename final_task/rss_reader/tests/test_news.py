"""
This module tests news module
"""

import re
import os
import sys

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

DIR = 'tests'

THIS_DIRECTORY = re.sub(DIR, '', THIS_DIRECTORY)

sys.path.append(THIS_DIRECTORY)


import unittest
import news


class NewsCheck(unittest.TestCase):
    def setUp(self) -> None:

        with open('news.log', 'w', encoding='utf-8') as file:
            file.write('Good url')

    def test_news_check(self):
        news_link = {'link': 'Good url'}

        self.assertEqual(news.news_check(news_link), True)

    def tearDown(self) -> None:
        os.remove('news.log')


class NewsPrint(unittest.TestCase):

    def test_news_print(self):
        self.assertEqual(news.news_print('21191125', 1), 2)

    def test_news_log(self):
        self.assertEqual(news.news_log_add('url'), None)


if __name__ == '__main__':
    unittest.main()