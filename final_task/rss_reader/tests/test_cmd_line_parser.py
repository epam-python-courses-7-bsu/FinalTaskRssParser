#!/usr/bin/env python3.8
"""Module for testing cmd_line_parser.py"""

import unittest
from unittest.mock import Mock

import cmd_line_parser as cml_parser
import rss_exceptions as er


class TestRSSReader(unittest.TestCase):
    """
    Tests functions from cmd_line_parser.py
    """

    def setUp(self):
        self.LOGGER = Mock()
        self.cmd_args = Mock()

    def test_convert_date(self):
        """
        Test convert_date(date)
        """
        date = Mock()

        date = '20191121'
        self.assertEqual(cml_parser.convert_date(date), '21 Nov 2019')

        date = '21 Nov 2019'
        with self.assertRaises(er.FormatDateError):
            cml_parser.convert_date(date)


if __name__ == '__main__':
    unittest.main()
