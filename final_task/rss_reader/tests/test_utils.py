#!/usr/bin/env python3.8
"""Module for testing utils.py"""

import unittest
from unittest.mock import patch, MagicMock

import utils


class TestOutPutTxtNews(unittest.TestCase):
    """
    Test function from utils.py
    """

    @patch('builtins.print', MagicMock())
    @patch('os.path.abspath')
    @patch('utils.FileSystemLoader')
    @patch('utils.Environment')
    def test_output_txt_news_not_color(self, env, file_sys_load, abspath):
        """
        Test output_txt_news_not_color(self, env, file_sys_load, abspath)
        if cmd_args.colorize is not set
        """
        cmd_args = MagicMock()
        cmd_args.colorize = False

        path_name = 'path_name'
        abspath.return_value = path_name

        all_news = {'test': 'news'}
        self.assertEqual(None, utils.output_txt_news(cmd_args, all_news))

        file_sys_load.assert_called_once_with((path_name + '/templates/'), followlinks=True)
        env.assert_called_once()

    @patch('builtins.print', MagicMock())
    @patch('os.path.abspath')
    @patch('utils.FileSystemLoader')
    @patch('utils.Environment')
    def test_output_txt_news_set_color(self, env, file_sys_load, abspath):
        """
        Test output_txt_news_not_color(self, env, file_sys_load, abspath)
        if cmd_args.colorize is set
        """
        cmd_args = MagicMock()
        cmd_args.colorize = True

        path_name = 'path_name'
        abspath.return_value = path_name

        all_news = {'test': 'news'}
        self.assertEqual(None, utils.output_txt_news(cmd_args, all_news))

        file_sys_load.assert_called_once_with((path_name + '/templates/'), followlinks=True)
        env.assert_called_once()


if __name__ == '__main__':
    unittest.main()
