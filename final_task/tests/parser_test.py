import unittest
from unittest.mock import patch
from feedparser import parse
from rss_reader import converter, news_parser
from expected_results import json_result, html_result


class TestParser(unittest.TestCase):

    def setUp(self):
        self.item = '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">' \
        '<channel><title>Yahoo News - Latest News &amp; Headlines</title>' \
        '<item><title>item_title</title>' \
    '<description>item_description</description>' \
    '<link>item_link</link><pubDate>item_date</pubDate>' \
    '<media:content url="media_link_url">media_link</media:content></item></channel>'
        self.parse_item = parse(self.item)


    def testGetDescription(self):
        self.assertEqual(news_parser.getDescription(self.parse_item.entries[0].description), 'item_description')
    

    def testJson(self):
        self.assertEqual(news_parser.intoJson(self.parse_item.entries[0]), json_result)
    

    def testCheckMediaContent(self):
        self.assertEqual(news_parser.checkMediaContent(self.parse_item.entries[0]), 'media_link_url')


    def testHtml(self):
        html_doc = converter.createHtmlStructure(self.parse_item, 1, 'html_path', '')
        self.assertEqual(html_doc, html_result)


    def testCacheNews(self):
        with patch("psycopg2.connect") as mock_connect:
            mock_con_cm = mock_connect.return_value
            mock_con = mock_con_cm.__enter__.return_value

            mock_cur_cm = mock_con.cursor.return_value
            mock_cur = mock_cur_cm.__enter__.return_value

            news_parser.cacheNews(self.parse_item)
            mock_connect.assert_called_with(database="postgres",user='postgres',password='rssreader',host='localhost',port='5432')
            mock_cur.executemany.called_with("INSERT INTO news VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING")
    

    def testInsertNewsIntoTable(self):
        item = '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">' \
        '<channel><title>Yahoo News - Latest News &amp; Headlines</title>' \
        '<item><title>item_title</title>' \
    '<description>item_description</description>' \
    '<link>item_link</link><pubDate>Mon, 25 Nov 2019 13:04:03</pubDate></item></channel>'
        parse_item = parse(item)
        news = news_parser.insertNewsIntoTable(parse_item)
        self.assertEqual(news, [('item_title', 'item_link', '', 'item_description', 1574676243.0)])


if __name__=='__main__':

    unittest.main()