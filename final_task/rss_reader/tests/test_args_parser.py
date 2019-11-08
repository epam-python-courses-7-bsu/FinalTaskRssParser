"""
This module tests args_parser module
"""

import unittest
import args_parser


class ARGSparser(unittest.TestCase):
    def test_get_parse(self):

        test_dict_1 = {
            'url': 'http://news.yahoo.com/rss/',
            'json': None,
            'verbose': None,
            'limit': 1,
            'date': None}

        input_1 = ['http://news.yahoo.com/rss/']

        test_dict_2 = {
            'url': 'http://news.yahoo.com/rss/',
            'json': True,
            'verbose': True,
            'limit': 9,
            'date': 20191107}

        input_2 = ['http://news.yahoo.com/rss/', '-j', '-b', '-l', '9', '-d', '20191107']
        input_3 = ['url', '-j', '999', '-b', '999', '-l', 'aaa']

        self.assertDictEqual(args_parser.get_parse(input_1), test_dict_1)
        self.assertDictEqual(args_parser.get_parse(input_2), test_dict_2)
        with self.assertRaises(SystemExit): args_parser.get_parse(input_3)

    def test_validate_url(self):

        self.assertEqual(args_parser.validate_url('https://news.yahoo.com/rss/'), True)
        self.assertEqual(args_parser.validate_url('www.wrongurl.com'), False)

    def test_validate_args(self):

        self.assertEqual(args_parser.validate_args({'limit': 9, 'date': 20191107}), True)
        self.assertEqual(args_parser.validate_args({'limit': -999, 'date': 20191107}), False)
        self.assertEqual(args_parser.validate_args({'limit': 9, 'date': 22191107}), False)
        self.assertEqual(args_parser.validate_args({'limit': -999, 'date': 21191107}), False)


if __name__ == '__main__':
    unittest.main()


