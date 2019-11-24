"""Module for testing pdf_converter"""
import datetime
import io
import os
import unittest
from unittest.mock import patch

import pdf_converter
from single_article import SingleArticle


class TestArticlesHandler(unittest.TestCase):
    """Tests pdf_converter"""
    def setUp(self) -> None:
        self.article1 = SingleArticle(feed='Yahoo News',
                                      feed_url='https://www.yahoo.com/news',
                                      title='House Democrats',
                                      date='Wed, 20 Nov 2019 20:54:24 -0500',
                                      link='https://news.yahoo.com/democrats.html',
                                      summary='Some text here1',
                                      links=[['https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8'
                                              '/Python_logo_and_wordmark.svg/1920px-Python_logo_and_wordmark.svg.png',
                                              'image'],
                                             ['https://news.yahoo.com/democrats.html', 'other']])

        self.article2 = SingleArticle(feed='Yahoo News',
                                      feed_url='https://www.yahoo.com/news',
                                      title='Trump',
                                      date='Fri, 22 Nov 2019 10:36:29 -0500',
                                      link='https://news.yahoo.com/trump.html',
                                      summary='Some text here1',
                                      links=[['https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8'
                                              '/Python_logo_and_wordmark.svg/1920px-Python_logo_and_wordmark.svg.png',
                                              'image'],
                                             ['https://news.yahoo.com/trump.html', 'other']])

    @patch('pdf_converter.FPDF.output')
    @patch('pdf_converter.datetime.date')
    @patch('pdf_converter.check_the_connection')
    def test_convert_to_pdf(self, mock_connection, mock_date, mock_output):
        """Testing conversion to pdf"""
        test_date = 'November 23, 2019'
        mock_date.today.return_value = datetime.datetime.strptime(test_date, '%B %d, %Y')

        path = os.path.abspath(os.path.dirname(__file__))
        test_path = os.path.join(path, test_date + ".pdf")

        mock_connection.return_value = 'not ok'
        mock_output.side_effect = PermissionError
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            pdf_converter.convert_to_pdf([self.article1, self.article2], path, None)
            expected_out = 'Please, close pdf file before converting or you need to run program as system ' \
                           'administrator, to save files in that location\n'
            self.assertEqual(fake_out.getvalue(), expected_out)


if __name__ == '__main__':
    unittest.main()
