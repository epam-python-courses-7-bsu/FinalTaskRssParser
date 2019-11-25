import argparse
import unittest
from unittest.mock import patch, call

from parser import check_digit, check_positive


class TestParser(unittest.TestCase):

    def test_check_digit(self):
        self.assertEqual(check_digit('5'), '5')
        self.assertEqual(check_digit('0'), '0')
        self.assertRaises(argparse.ArgumentTypeError, check_digit, '*')
        self.assertRaises(argparse.ArgumentTypeError, check_digit, 'a')

    def test_check_positive(self):
        self.assertEqual(check_positive('5'), 5)
        self.assertRaises(argparse.ArgumentTypeError, check_positive, '-5')
        with patch('parser.check_digit') as mocked_check:
            check_positive('100')
            mocked_check.assert_called_with('100')


if __name__ == "__main__":
    unittest.main()
