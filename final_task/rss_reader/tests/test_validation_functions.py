""" Testing module for validation functions. """
import unittest
from unittest import mock

import requests
import validation_functions as val_func
import exceptions as exc


class TestValidationFunctions(unittest.TestCase):
    """  Class for testing some validation functions.  """

    def setUp(self):
        self.logger = mock.Mock()
        self.com_line_args = mock.Mock()

    def test_check_internet_connection(self):
        with mock.patch('requests.get'):
            self.assertTrue(val_func.check_internet_connection(self.logger))

        with self.assertRaises(exc.Error):
            with mock.patch('requests.get', side_effect=requests.ConnectionError):
                val_func.check_internet_connection(self.logger)

    def test_check_emptiness(self):
        with self.assertRaises(exc.Error):
            news_collection = []
            val_func.check_emptiness(news_collection, self.logger)

        news_collection = ["Smile"]
        self.assertTrue(val_func.check_emptiness(news_collection, self.logger))

    @mock.patch('urllib.request.Request', side_effect=ValueError)
    def test_check_url_Request(self, req):
        with self.assertRaises(exc.Error):
            val_func.check_url(self.com_line_args, self.logger)

    def test_check_limit_arg(self):
        self.com_line_args.limit = 0
        self.assertTrue(val_func.check_limit_arg(self.com_line_args, self.logger))

        self.com_line_args.limit = 5
        self.assertTrue(val_func.check_limit_arg(self.com_line_args, self.logger))

        self.com_line_args.limit = None
        self.assertFalse(val_func.check_limit_arg(self.com_line_args, self.logger))

        with self.assertRaises(exc.ComLineArgError):
            self.com_line_args.limit = -5
            val_func.check_limit_arg(self.com_line_args, self.logger)

    def test_check_date_arg(self):
        self.com_line_args.date = "20190111"
        self.assertTrue(val_func.check_date_arg(self.com_line_args, self.logger))
        self.com_line_args.date = ""
        self.assertFalse(val_func.check_date_arg(self.com_line_args, self.logger))


if __name__ == '__main__':
    unittest.main()



