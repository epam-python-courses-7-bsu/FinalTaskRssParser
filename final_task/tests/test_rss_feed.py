import sys
import unittest
from io import StringIO
from unittest.mock import patch, mock_open

sys.path.insert(1, 'final_task/rss_reader')
from rss_feed import RssFeed
from rss_reader import init_feed


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
            feed.to_json()
            self.assertEqual(fake_out.getvalue(), result)

    def test_cache(self):
        news_feed = init_feed('final_task/tests/test_feed.xml', 2)
        expected_result = '{\n'\
            '    "_default": {\n'\
            '        "1": {\n'\
            '            "date": "20031231",\n'\
            '            "link": "ITEM1 LINK",\n'\
            '            "media": "http://www.foo.com/bar.jpg",\n'\
            '            "published": "2003-12-31",\n'\
            '            "source": "final_task/tests/test_feed.xml",\n'\
            '            "title": "ITEM1 TITLE"\n'\
            '        },\n'\
            '        "2": {\n'\
            '            "date": "20031231",\n'\
            '            "link": "ITEM2 LINK",\n'\
            '            "media": "http://www.foo.com/bar.jpg",\n'\
            '            "published": "2003-12-31",\n'\
            '            "source": "final_task/tests/test_feed.xml",\n'\
            '            "title": "ITEM2 TITLE"\n'\
            '        }\n'\
            '    }\n'\
            '}'
        news_feed.cache('test_db.json')

        with open('test_db.json') as fp:
            result = fp.read()
        self.assertEqual(result, expected_result)
        pass
