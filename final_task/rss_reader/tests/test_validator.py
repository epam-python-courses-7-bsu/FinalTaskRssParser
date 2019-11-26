#!/usr/bin/env python3.8
"""Module for testing validator.py"""

import unittest
from unittest.mock import patch, Mock

import requests

import validator
import rss_exceptions as er


class TestCheckFunctions(unittest.TestCase):
    """
    Tests functions from validator.py
    """

    def setUp(self):
        self.cmd_args = Mock()

    def test_check_internet_connection(self):
        """
        Test check_internet_connection()
        """
        # If internet is available, return True
        with patch('requests.get'):
            self.assertTrue(validator.check_internet_connection())

        # If internet is unavailable - raise InternetConnectionError, return None
        with self.assertRaises(er.InternetConnectionError):
            with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
                self.assertIsNone(validator.check_internet_connection())

    def test_check_url_availability(self):
        """
        Test check_url_availability(cmd_args)
        """
        # if URL is not defined
        self.cmd_args.source = False
        with self.assertRaises(er.UndefinedURL):
            validator.check_url_availability(self.cmd_args)

        # if URL is defined
        self.cmd_args.source = True
        # if URL is available, return True
        with patch('requests.get'):
            self.assertTrue(validator.check_url_availability(self.cmd_args))

        # if URL is unavailable, raise UnreachableURLError, return None
        with self.assertRaises(er.UnreachableURLError):
            with patch('requests.get', side_effect=Exception):
                self.assertIsNone(validator.check_url_availability(self.cmd_args))

    def mock_status_code_200(self, *args):
        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 200
        return response_mock

    def mock_status_code_404(self, *args):
        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.raise_for_status.side_effect = er.URLResponseError
        return response_mock

    @patch('requests.get')
    def test_check_response_status_code(self, get_mock):
        """
        Test check_response_status_code(cmd_args)
        """
        # if status code is 200: OK, return True

        get_mock.side_effect = self.mock_status_code_200

        self.assertTrue(validator.check_response_status_code(self.cmd_args))

        # if status code is greater than 400 - raise URLResponseError, return None
        get_mock.side_effect = self.mock_status_code_404
        with self.assertRaises(er.URLResponseError):
            self.assertIsNone(validator.check_response_status_code(self.cmd_args))

    def test_check_limit_value(self):
        """
        Test check_limit_value(limit)
        """
        limit = Mock()

        # if limit value is a positive - return True
        limit = 10
        self.assertTrue(validator.check_limit_value(limit))

        # if limit value is None - return True
        limit = None
        self.assertTrue(validator.check_limit_value(limit))

        # if limit value is a negative - raise LimitSignError, return None
        limit = -2
        with self.assertRaises(er.LimitSignError):
            self.assertIsNone(validator.check_limit_value(limit))

    def test_check_news_collection(self):
        """
        Test check_news_collection(news_collection)
        """
        news_collection = Mock()

        # if news_collection is empty, raise FeedError, return None
        news_collection = []
        with self.assertRaises(er.FeedError):
            self.assertIsNone(validator.check_news_collection(news_collection))

        # if news_collection is not empty, return True
        news_collection = [1]
        self.assertTrue(validator.check_news_collection(news_collection))


if __name__ == '__main__':
    unittest.main()
