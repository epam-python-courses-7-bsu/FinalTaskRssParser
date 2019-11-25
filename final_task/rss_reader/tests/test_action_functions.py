""" Testing module for action functions. """
import unittest
from unittest import mock
import action_functions as act_func
import exceptions as exc


class TestActionFunctions(unittest.TestCase):
    """ Class for testing some of action functions. """
    def setUp(self):
        self.logger = mock.Mock()
        self.com_line_args = mock.Mock()

    def test_get_limit_news_collection(self):
        news_collection = [num for num in range(10)]

        with mock.patch('validation_functions.check_limit_arg') as check_limit_mock:
            check_limit_mock.return_value = True
            self.com_line_args.limit = 4
            self.assertEqual(len(act_func.get_limit_news_collection
                                 (news_collection, self.com_line_args, self.logger)), 4)
            self.com_line_args.limit = 11
            self.assertEqual(len(act_func.get_limit_news_collection
                                 (news_collection, self.com_line_args, self.logger)), 10)

            check_limit_mock.return_value = False
            self.assertEqual(len(act_func.get_limit_news_collection
                                 (news_collection, self.com_line_args, self.logger)), 10)

    def test_clean_str(self):
        test_str = "Netanyahu \u2014rival seeks support from PM&#39;s party to form government."
        expect_str = "Netanyahu rival seeks support from PM's party to form government."
        self.assertEqual(act_func.clean_str(test_str), expect_str)

    def test_convert_date(self):
        self.assertEqual(act_func.convert_date("20190207"), "7 Feb 2019")
        self.assertEqual(act_func.convert_date("20190410"), "10 Apr 2019")
        with self.assertRaises(exc.Error):
            act_func.convert_date("2000")


if __name__ == '__main__':
    unittest.main()
