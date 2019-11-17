import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from classes.rss_feed import RssFeed


class TestRssFeed(unittest.TestCase):

    def test_printfeed(self):
        title = 'title'
        description = 'description'
        link = 'link'
        news_list = [1, 2, 3]

        result = '\n'
        result += ' '*36 + title + '\n'
        result += ' '*36 + '='*len(title) + '\n'
        result += ' '*int(abs((36 + len(title)/2 - len(description)/2))) + description + '\n\n'
        result += '='*120 + '\n'
        for _, item in enumerate(news_list):
            result += str(item) + '\n'
            result += '='*120 + '\n'
        result += '\n'

        feed = RssFeed(title, description, link, news_list)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            feed.print_feed()
            self.assertEqual(fake_out.getvalue(), result)

    def test_tojson(self):
        feed = RssFeed('title', 'description', 'link', [1, 2, 3])
        result = '{\n    '\
            '"description": "description",\n    '\
            '"link": "link",\n    '\
            '"news_list": [\n        1,\n        2,\n        3\n    ],'\
            '\n    "title": "title"\n}'
        result += '\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            feed.toJSON()
            self.assertEqual(fake_out.getvalue(), result)
