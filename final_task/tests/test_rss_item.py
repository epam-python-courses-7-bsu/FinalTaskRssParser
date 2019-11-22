import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from rss_item import RssItem


class TestRssItem(unittest.TestCase):

    def setUp(self):
        self.item = RssItem('title', 'date', 'description', 'link', 'media', 'source', 'date_parsed', 'base64 image')

    def test_string(self):
        expected_result = 'TITLE: title\
            \n\t|| DESCRIPTION: description\
            \n\t|| PUBLISHED: date\
            \n\t|| LINK: link\
            \n\t|| MEDIA: media'
        self.assertEqual(self.item.__str__(), expected_result)

    def test_to_json(self):
        expected_result = '{\n'\
            '    "date": "date_parsed",\n'\
            '    "description": "description",\n'\
            '    "img": "base64 image",\n'\
            '    "link": "link",\n'\
            '    "media": "media",\n'\
            '    "published": "date",\n'\
            '    "source": "source",\n'\
            '    "title": "title"\n'\
            '}\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.item.to_json()
            self.assertEqual(fake_out.getvalue(), expected_result)
