import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from rss_item import RssItem


class TestRssItem(unittest.TestCase):

    def test_string(self):
        item = RssItem('title', 'date', 'link', 'media', 'source', 'date_parsed')
        expected_result = 'TITLE: title\
            \n\t|| PUBLISHED: date \
            \n\t|| LINK: link\
            \n\t|| MEDIA: media'
        self.assertEqual(item.__str__(), expected_result)
