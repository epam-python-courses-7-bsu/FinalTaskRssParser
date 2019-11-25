"""Module for testing main module"""
import argparse
import io
import sys
import os
import unittest
from unittest.mock import patch, Mock

import rss_reader


class TestArticlesHandler(unittest.TestCase):
    """Tests rss_reader"""

    def test_main(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test_path1 = os.path.join(path, 'data_for_testing', "rss1.xml")

        argparse.ArgumentParser.parse_args.source = Mock(return_value=test_path1)

        test_args = ["rss_reader.py", 'https://news.tut.by/rss/index.rss', '--limit', '1']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                rss_reader.main()
                expected_out_path = os.path.join(path, 'expected_result_files', 'rss_reader_expected_out_1.txt')
                with io.open(expected_out_path, 'r', encoding='utf-8-sig') as out_file:
                    expected_out = out_file.read()
            self.assertEqual(fake_out.getvalue(), expected_out)

        test_args = ["rss_reader.py", 'https://news.tut.by/rss/index.rss', '--limit', '3']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                rss_reader.main()
                expected_out_path = os.path.join(path, 'expected_result_files', 'rss_reader_expected_out_2.txt')
                with io.open(expected_out_path, 'r', encoding='utf-8-sig') as out_file:
                    expected_out = out_file.read()
            self.assertEqual(fake_out.getvalue(), expected_out)

        test_args = ["rss_reader.py", 'https://news.tut.by/rss/index.rss', '--date', '20191123', '--limit', '2']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                rss_reader.main()
                expected_out_path = os.path.join(path, 'expected_result_files', 'rss_reader_expected_out_3.txt')
                with io.open(expected_out_path, 'r', encoding='utf-8-sig') as out_file:
                    expected_out = out_file.read()
            self.assertEqual(fake_out.getvalue(), expected_out)

        test_args = ["rss_reader.py", 'https://news.tut.by/rss/index.rss', '--date', '20191124', '--limit', '2',
                     '--json']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                rss_reader.main()
                expected_out_path = os.path.join(path, 'expected_result_files', 'rss_reader_expected_out_4.txt')
                with io.open(expected_out_path, 'r', encoding='utf-8-sig') as out_file:
                    expected_out = out_file.read()
            self.assertEqual(fake_out.getvalue(), expected_out)


if __name__ == '__main__':
    unittest.main()
