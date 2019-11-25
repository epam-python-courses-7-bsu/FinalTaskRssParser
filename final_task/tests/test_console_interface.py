import sys
sys.path.insert(1, 'final_task/rss_reader')
from console_interface import *
import unittest
import argparse
from unittest import mock


class TestParsArgs(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(source="https://news.yahoo.com/rss/", version='1.4.2', json=False,
                                                verbose=False, limit=5, date="20191123", to_html=False, to_pdf=True,
                                                path=r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task"))

    def test_parsing(self, mock_args):
        args = parse_args()
        self.assertEqual(args.source, "https://news.yahoo.com/rss/")
        self.assertEqual(args.limit, 5)
        self.assertEqual(args.date, "20191123")
        self.assertEqual(args.version, "1.4.2")
        self.assertEqual(args.json, False)
        self.assertEqual(args.verbose, False)
        self.assertEqual(args.to_pdf, True)
        self.assertEqual(args.to_html, False)
        self.assertEqual(args.path, r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task")

if __name__ == '__main__':
    unittest.main()