import unittest
from unittest.mock import patch
from rss_reader import get_cache
from expected_results import html_result_from_db


class TestParser(unittest.TestCase):

    def testGetCacheFromDB(self):
        with patch("psycopg2.connect") as mock_connect:
            expected = ['title', 'link', 'image', 'description']

            mock_con_cm = mock_connect.return_value
            mock_con = mock_con_cm.__enter__.return_value

            mock_cur_cm = mock_con.cursor.return_value
            mock_cur = mock_cur_cm.__enter__.return_value

            mock_cur.fetchall.return_value = expected

            result = get_cache.getCacheFromDB('20191125')
            self.assertEqual(result, expected)

            mock_connect.assert_called_with(database="postgres",user='postgres',password='rssreader',host='localhost',port='5432')


    def testCollectNewsFromDB(self):
        with patch('rss_reader.get_cache.getCacheFromDB') as mock_cache:
            mock_cache.return_value = [('title', 'link', 'image', 'description')]

            expected = ['Cache News: ', '', '\nTitle: title', '\nLink: link\n', 'Description: description\n']

            result = get_cache.collectNewsFromDB(1, False, ['','',''], '20191125')
            self.assertEqual(result, expected)

            expectedJson = ['Cache News: ', '', '{"Title: ": "title", "Link: ": "link", "Description": "description"}']

            result = get_cache.collectNewsFromDB(1, True, ['','',''], '20191125')
            self.assertEqual(result, expectedJson)


    def testCreateHtmlFromDB(self):
        with patch('rss_reader.get_cache.getCacheFromDB') as mock_cache:
            mock_cache.return_value = [('item_title', 'item_link', '', 'item_description')]

            expected = html_result_from_db

            result = get_cache.createHtmlFromDB(1, 'html_path', '', '20191125')
            self.assertEqual(result, expected)


    def testDateToStamp(self):
        expected = 1574629200.0
        result = get_cache.dateToStamp('20191125')

        self.assertEqual(result, expected)


if __name__=='__main__':

    unittest.main()

