import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from classes.rss_item import RssItem

class TestRssItem(unittest.TestCase):
    
    def test_formatstring(self):
        expected_result = '<<<>>>&&\"\"\'\''
        data = '&#60;&#x3c;&#x3C;&#62;&#x3e;&#x3E;&#38;&#x26;&#34;&#x22;&#39;&#x27;'
        item = RssItem('title', 'date', 'link', 'media')
        result = item.format_data(data)
        self.assertEqual(result, expected_result)

    def test_string(self):
        item = RssItem('title', 'date', 'link', 'media')
        expected_result = 'TITLE: title\
            \n\t|| PUBLISHED: date \
            \n\t|| LINK: link\
            \n\t|| MEDIA: media'
        self.assertEqual(item.__str__(), expected_result)
