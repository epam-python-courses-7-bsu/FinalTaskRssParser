"""Module for testing functions from check_funk.py"""

import unittest
from unittest.mock import patch, Mock
import functions.check_func as ch_f
import requests
import classes.exceptions as exc
import feedparser


class TestCheckFunctions(unittest.TestCase):
    """Tests functions from check_func.py"""

    def setUp(self):
        self.logger = Mock()
        self.command_line_args = Mock()

    def test_check_internet_connection(self):

        #If internet is avaliable should return True
        self.assertTrue(ch_f.check_internet_connection(self.logger))

        # If internet is not avaliable should raise InternetConnectionError
        with self.assertRaises(exc.InternetConnectionError):
            with patch('requests.get', side_effect=requests.ConnectionError):
                ch_f.check_internet_connection(self.logger)


    def test_check_version_argument(self):

        # If version argument print should print version and raise SystemExit
        self.command_line_args.version = True
        with patch('builtins.print'):
            with self.assertRaises(exc.VersionPrinted):
                ch_f.check_version_argument(self.command_line_args)

        # If version argument is False, return None
        self.command_line_args.version = False
        self.assertIsNone(ch_f.check_version_argument(self.command_line_args))

    def test_check_verbose(self):

        # If verbose, should set level to 20
        self.command_line_args.verbose = True
        logger = ch_f.check_verbose(self.command_line_args)
        self.assertEqual(logger.getEffectiveLevel(), 20)

        # If not verbose, level should be 30
        self.command_line_args.verbose = False
        logger = ch_f.check_verbose(self.command_line_args)
        self.assertEqual(logger.getEffectiveLevel(), 30)


    def test_check_feed_status(self):

        feed = Mock()

        # If feed.status not between (400:600), return feed
        feed.status = 200
        self.assertEqual(ch_f.check_feed_status(feed), feed)

        # If feed.status between (400:600), should raise GettingFeedError
        feed.status = 404
        with self.assertRaises(exc.GettingFeedError):
            ch_f.check_feed_status(feed)

        # If getting feed.status raises AttributeError, should raises UrlError
        feed = feedparser.parse("some_invalid_url")
        with self.assertRaises(exc.UrlError):
            ch_f.check_feed_status(feed)

    def check_news_collection(news_collection, logger):
        """Check if news_collection is not empty"""
        if not news_collection:
            raise exc.FeedXmlError("Parsed xml is not valid")
        else:
            logger.info("Successful collected.")

    def test_check_news_collection(self):

        # If news_collection if empty, raises SystemExit
        news_collection = []
        with self.assertRaises(exc.FeedXmlError):
            ch_f.check_news_collection(news_collection, self.logger)

        # If news_collection is True, return None
        news_collection = [1]
        self.assertIsNone(ch_f.check_news_collection(news_collection, self.logger))


if __name__ == '__main__':
    unittest.main()
