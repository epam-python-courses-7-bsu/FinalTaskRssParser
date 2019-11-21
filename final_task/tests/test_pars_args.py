import sys

sys.path.insert(1, 'final_task/rss_reader')
from pars_args import *
import unittest
import argparse
from unittest import mock  # python 3.3+


class TestParsArgs(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(source='https://news.tut.by/rss/',
                                                version='2.0',
                                                json=False,
                                                verbose = False,
                                                limit=2,
                                                date="20191212"))
    def test_command(self, mock_args):
        data = get_args()
        self.assertEqual(data.source, "https://news.tut.by/rss/")
        self.assertEqual(data.version, "2.0")
        self.assertEqual(data.json, False)
        self.assertEqual(data.verbose, False)
        self.assertEqual(data.limit, 2)
        self.assertEqual(data.date, "20191212")
