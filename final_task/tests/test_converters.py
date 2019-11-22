import sys
import os
import unittest
from io import StringIO
from unittest.mock import patch

import requests

sys.path.insert(1, 'final_task/rss_reader')
from converters import get_image_path, get_html_doc, path_validation
from rss_feed import RssFeed
from exceptions_ import ConvertionError
from rss_reader import init_feed

class TestConverters(unittest.TestCase):

    def test_get_image_url(self):
        url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
        expected_result = 'temp-img' + str(hash(url)) + '.jpg'
        result = get_image_path(url)
        self.assertEqual(result, expected_result)
        os.remove('temp-img' + str(hash(url)) + '.jpg')

    def test_get_html_doc(self):
        feed = init_feed('final_task/tests/test_feed.xml', 2)
        expected_result = '<!DOCTYPE html>\n'\
            '<html>\n'\
            '  <head>\n'\
            '    <title>RSS FEED</title>\n'\
            '  </head>\n'\
            '  <body>\n'\
            '    <h1>News:</h1>\n'\
            '    <div>\n'\
            '      <h3>ITEM1 TITLE</h3>\n'\
            '      <h5>IMAGE</h5>\n'\
            '      <img src="data:image/png;base64, bm90IGZvdW5k">\n'\
            '      <h5>DESCRIPTION: </h5>\n'\
            '      <p>unknown</p>\n'\
            '      <p>2003-12-31</p>\n'\
            '      <p>SOURCE: final_task/tests/test_feed.xml</p>\n'\
            '      <a href="ITEM1 LINK">LINK</a>\n'\
            '    </div>\n'\
            '    <div>\n'\
            '      <h3>ITEM2 TITLE</h3>\n'\
            '      <h5>IMAGE</h5>\n'\
            '      <img src="data:image/png;base64, bm90IGZvdW5k">\n'\
            '      <h5>DESCRIPTION: </h5>\n'\
            '      <p>unknown</p>\n'\
            '      <p>2003-12-31</p>\n'\
            '      <p>SOURCE: final_task/tests/test_feed.xml</p>\n'\
            '      <a href="ITEM2 LINK">LINK</a>\n'\
            '    </div>\n'\
            '  </body>\n'\
            '</html>'
        result = get_html_doc(feed.get_news_as_dicts(2))
        self.assertEqual(result, expected_result)

    def test_path_validation(self):
        with self.assertRaises(ConvertionError):
            path_validation('asdasdas', True)
