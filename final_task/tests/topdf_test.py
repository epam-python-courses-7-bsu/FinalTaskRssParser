import unittest
from unittest.mock import patch
from rss_reader import topdf
from expected_results import html_result 


class TestParser(unittest.TestCase):

    @patch('rss_reader.topdf.datetime')
    @patch('builtins.open')
    def testConvertToPdf(self, mock_file, mock_time):
        mock_time.strftime.return_value = '191749'

        result = topdf.convertHtmlToPdf(html_result, 'pdf_path/')
        expected = 'NewsFeed-191749.pdf'

        mock_file.assert_called_with('pdf_path/NewsFeed-191749.pdf', "w+b")
        self.assertEqual(result, expected)


    def testSplitHost(self):
        url = 'https://news.yahoo.com/rss'
        expected = ('news.yahoo.com', '/rss')
        result = topdf.splithost_polyfill(url)
        self.assertEqual(result, expected)


if __name__=='__main__':

    unittest.main()
