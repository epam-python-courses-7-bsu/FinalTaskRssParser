"""Module for testing argparse_handler functions"""
import datetime
import sys
import unittest
from unittest.mock import patch
import urllib.request

import argparse_handler
import custom_error


class TestArgparseHandler(unittest.TestCase):
    """Tests argparse_handler functions"""
    def test_check_if_date_in_arguments(self):
        """Testing --date in arguments"""
        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertFalse(argparse_handler.check_if_date_in_arguments())
        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--verbose", '--date']
        with patch.object(sys, 'argv', test_args):
            self.assertTrue(argparse_handler.check_if_date_in_arguments())

    def test_check_if_help_or_version_in_arguments(self):
        """Testing --help, -h or --version in arguments"""
        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--help"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_help_or_version_in_arguments(), 'help')

        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "-h"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_help_or_version_in_arguments(), 'help')

        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--version"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_help_or_version_in_arguments(), 'version')

        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss']
        with patch.object(sys, 'argv', test_args):
            self.assertIsNone(argparse_handler.check_if_help_or_version_in_arguments())

    def test_check_the_arguments_amount(self):
        """Testing if error raises when not enough arguments"""
        test_args = []
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(custom_error.NotEnoughArgumentsError):
                argparse_handler.check_the_arguments_amount()

        test_args = ["rss_reader.py"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(custom_error.NotEnoughArgumentsError):
                argparse_handler.check_the_arguments_amount()

    def test_link_found(self):
        """Testing if link found correctly"""
        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertTrue(argparse_handler.link_found())

        test_args = ["rss_reader.py", "--verbose", '--date', '\'https://news.tut.by/index.rss\'']
        with patch.object(sys, 'argv', test_args):
            self.assertTrue(argparse_handler.link_found())
            self.assertEqual(test_args, ["rss_reader.py", 'https://news.tut.by/index.rss', "--verbose", '--date'])

        test_args = ["rss_reader.py", 'tut by', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertFalse(argparse_handler.link_found())

    @patch('argparse_handler.check_if_help_or_version_in_arguments')
    def test_check_if_url_or_date_in_arguments(self, mock_help_version):
        """Testing different initial arguments values"""
        mock_help_version.return_value = None

        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_url_or_date_in_arguments(), 'link_only')

        test_args = ["rss_reader.py", 'abc', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(custom_error.UrlNotFoundInArgsError):
                argparse_handler.check_if_url_or_date_in_arguments()

        test_args = ["rss_reader.py", '--date', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_url_or_date_in_arguments(), 'date_only')

        test_args = ["rss_reader.py", 'https://news.tut.by/index.rss', '--date', "--verbose"]
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(argparse_handler.check_if_url_or_date_in_arguments(), 'link_and_date')

        mock_help_version.return_value = 'flag'
        self.assertEqual(argparse_handler.check_if_url_or_date_in_arguments(), 'flag')

    @patch('argparse_handler.urllib.request.urlopen')
    def test_check_the_connection(self, mock_urlopen):
        """Testing with good connection, with HTTPError and with URLError """
        self.assertEqual(argparse_handler.check_the_connection('https://news.tut.by/'), (True, 'connection success'))

        mock_urlopen.side_effect = urllib.request.HTTPError(None, '404', 'Not found', None, None)
        self.assertEqual(argparse_handler.check_the_connection('https://news.tut.by/404'),  (False, '404: Not found'))

        mock_urlopen.side_effect = urllib.request.URLError('message')
        self.assertEqual(argparse_handler.check_the_connection('https://news'), (False, 'message'))

    def test_check_if_url_is_valid(self):
        """Testing different links"""
        self.assertFalse(argparse_handler.check_if_url_is_valid('https'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('https://'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('https://news'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('news.tut.by/rss/index.rss'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('https://newstutby/rss/index.rss'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('https://n./rss/index.rss'))
        self.assertFalse(argparse_handler.check_if_url_is_valid('https://.n/rss/index.rss'))
        self.assertTrue(argparse_handler.check_if_url_is_valid('https://news.tut.by/rss/index.rss'))
        self.assertTrue(argparse_handler.check_if_url_is_valid('https://news.tut.by/'))
        self.assertTrue(argparse_handler.check_if_url_is_valid('https://n.t/rss/index.rss'))

    @patch('argparse_handler.check_if_url_is_valid')
    @patch('argparse_handler.check_the_connection')
    def test_valid_url(self, mock_connection, mock_url_is_valid):
        """Testing good url, bad connection, not valid url"""
        mock_url_is_valid.return_value = True
        mock_connection.return_value = (True, 'ss')
        self.assertEqual(argparse_handler.valid_url('https://news.tut.by/'), 'https://news.tut.by/')

        mock_connection.return_value = (False, 'error')
        with self.assertRaises(custom_error.ConnectionFailedError):
            argparse_handler.valid_url('https://news.tuuut.by/')

        mock_url_is_valid.return_value = False
        with self.assertRaises(custom_error.NotValidUrlError):
            argparse_handler.valid_url('https://news/')

    def test_valid_limit(self):
        """Testing different limit values"""
        self.assertEqual(argparse_handler.valid_limit('3'), 3)

        with self.assertRaises(custom_error.NotValidLimitError):
            argparse_handler.valid_limit('3.3')

        with self.assertRaises(custom_error.NotValidLimitError):
            argparse_handler.valid_limit('0')

        with self.assertRaises(custom_error.NotValidLimitError):
            argparse_handler.valid_limit('-1')

        with self.assertRaises(custom_error.NotValidLimitError):
            argparse_handler.valid_limit('aa')

    def test_valid_date(self):
        """Testing different dates"""
        self.assertEqual(argparse_handler.valid_date('20191120'), datetime.datetime.strptime('20191120', "%Y%m%d"))

        with self.assertRaises(custom_error.NotValidDateError):
            argparse_handler.valid_date('201911')

        with self.assertRaises(custom_error.NotValidDateError):
            argparse_handler.valid_date('201911201800')

        with self.assertRaises(custom_error.NotValidDateError):
            argparse_handler.valid_date('aaaaaa')

        with self.assertRaises(custom_error.NotValidDateError):
            argparse_handler.valid_date('20191199')

    @patch('argparse_handler.os.path')
    def test_valid_directory_path(self, mock_os_path):
        """Testing directory existence, os separator adding and raising error if directory not exists"""
        mock_os_path.isdir.return_value = True
        mock_os_path.sep = "/"

        self.assertEqual(argparse_handler.valid_directory_path('path'), 'path/')
        self.assertEqual(argparse_handler.valid_directory_path('path/'), 'path/')

        mock_os_path.isdir.return_value = False
        with self.assertRaises(custom_error.NotValidPathError):
            argparse_handler.valid_directory_path('dsf.dfe2')


if __name__ == '__main__':
    unittest.main()
