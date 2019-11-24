"""Module for testing html_converter"""
import datetime
import io
import os
import unittest
from unittest.mock import patch, call

import html_converter
from single_article import SingleArticle


class TestArticlesHandler(unittest.TestCase):
    """Tests html_converter"""
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

    @patch('html_converter.open', new_callable=unittest.mock.mock_open)
    @patch('html_converter.datetime.date')
    @patch('html_converter.check_the_connection')
    def test_convert_to_html(self, mock_connection, mock_date, mock_open_file):
        """Testing conversion to html with/without connection"""
        mock_connection.return_value = 'ok'

        test_date = 'November 23, 2019'
        mock_date.today.return_value = datetime.datetime.strptime(test_date, '%B %d, %Y')

        path = os.path.abspath(os.path.dirname(__file__))
        test_path1 = os.path.join(path, test_date + ".html")

        with open(os.path.join(path, 'expected_result_files', 'html_converter_expected_result1.html'),
                  'r', encoding="utf-8") as the_file:
            expected_result1 = the_file.read()

        calls = [call(str(expected_result1))]

        html_converter.convert_to_html([self.article1, self.article2], path, None)

        mock_open_file.assert_called_with(test_path1, 'w', encoding='utf-8')
        mock_open_file().write.assert_has_calls(calls)

        self.article1.links[0][0] = 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif'
        source_url = 'https://www.yahoo.com/news'
        test_path2 = os.path.join(path, test_date + " www.yahoo.com.html")
        with open(os.path.join(path, 'expected_result_files', 'html_converter_expected_result2.html'),
                  'r', encoding="utf-8") as the_file:
            expected_result2 = the_file.read()

        calls = [call(str(expected_result2))]

        html_converter.convert_to_html([self.article1, self.article2], path, source_url)

        mock_open_file.assert_called_with(test_path2, 'w', encoding='utf-8')
        mock_open_file().write.assert_has_calls(calls)

        mock_connection.return_value = 'not ok'
        with open(os.path.join(path, 'expected_result_files', 'html_converter_expected_result3.html'),
                  'r', encoding="utf-8") as the_file:
            expected_result3 = the_file.read()

        calls = [call(str(expected_result3))]

        html_converter.convert_to_html([self.article1, self.article2], path, source_url)

        mock_open_file.assert_called_with(test_path2, 'w', encoding='utf-8')
        mock_open_file().write.assert_has_calls(calls)

        mock_open_file.side_effect = PermissionError
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            html_converter.convert_to_html([self.article1, self.article2], path, source_url)
            expected_out = 'You need to run program as system administrator, to save files in that location\n'
            self.assertEqual(fake_out.getvalue(), expected_out)


if __name__ == '__main__':
    unittest.main()
