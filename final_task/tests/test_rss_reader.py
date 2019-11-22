import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from rss_reader import init_feed, init_news_list
from rss_item import RssItem


class TestRssReader(unittest.TestCase):

    def test_init_feed(self):
        news_feed = init_feed('final_task/tests/test_feed.xml', 2)
        rss_items = [
            RssItem('ITEM1 TITLE', '2003-12-31', 'unknown', 'ITEM1 LINK',
                    'http://www.foo.com/bar.jpg', 'final_task/tests/test_feed.xml', '20031231', 'b\'bm90IGZvdW5k\''),

            RssItem('ITEM2 TITLE', '2003-12-31', 'unknown', 'ITEM2 LINK',
                    'http://www.foo.com/bar.jpg', 'final_task/tests/test_feed.xml', '20031231', 'b\'bm90IGZvdW5k\'')
            ]
        self.assertEqual(news_feed.title, 'CHANNEL TITLE')
        self.assertEqual(news_feed.description, 'CHANNEL DESCRIPTION')
        self.assertEqual(news_feed.link, 'CHANNEL LINK')
        self.assertEqual(news_feed.news_list, rss_items)
