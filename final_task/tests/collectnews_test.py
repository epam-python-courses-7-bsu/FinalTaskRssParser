import unittest
from unittest.mock import patch
from feedparser import parse
from rss_reader import collect_news
from expected_results import normal_result, json_result, html_result


class TestParser(unittest.TestCase):
    def setUp(self):
        self.item = '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">' \
        '<channel><title>Yahoo News - Latest News &amp; Headlines</title>' \
        '<item><title>item_title</title>' \
    '<description>item_description</description>' \
    '<link>item_link</link><pubDate>item_date</pubDate>' \
    '<media:content url="media_link_url">media_link</media:content></item></channel>'
        self.parse_item = parse(self.item)


    def testCollectNews(self):
        self.assertEqual(collect_news.collectNews(1, False, '', '', ['','',''], self.item), normal_result)
        self.assertEqual(collect_news.collectNews(1, True, '', '', ['','',''], self.item)[2], json_result)
        self.assertEqual(collect_news.collectNews(1, False, 'tohtml', '', ['','',''], self.item), html_result)


if __name__=='__main__':

    unittest.main()