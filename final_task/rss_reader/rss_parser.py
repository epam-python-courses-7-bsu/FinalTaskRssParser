#!/usr/bin/env python3.8

import html
from os import path

from bs4 import BeautifulSoup
import feedparser
from jinja2 import Environment, FileSystemLoader
import requests

from rss_exceptions import InvalidURL, FeedError


class RSSparser:
    """
    Parsed the RSS news from received link, extracts required amount of news and prints result
    in human readable format.

    Parameters:
        args: dict: parsed arguments out of sys.argv;
        logger: LOGGER: tracks events that occur during program execution.

    Returns:
        store_news: list of dictionaries with extracted info of required amount of parsed news;
        output_txt_news method returns result in human readable format (filling the prepared).
    """

    def __init__(self, args, logger):
        self.url = args.source
        self.limit = args.limit
        self.logger = logger

        self.logger.info(f'Get RSS_url {self.url} and value = {self.limit} (limits amount of output news)')

        self.check_the_connection(self.url, self.logger)
        self.response = self.get_the_response(self.url, self.logger)

        # Extract the news-site name converting it to the unicode
        self.feed_name = html.unescape(self.response.feed.get('title', ''))
        # Extract all news separately in one list

        self.logger.info('Separate a news from the URL.')

        self.news = self.response.entries
        self.check_news_collection(self.news, self.logger)

        self.limit = self.check_limit_value(self.limit)
        self.all_news = self.parse_feed()

    @staticmethod
    def check_the_connection(url, logger):
        """
        Check the internet connection
        :param url: str
        :param logger: logger
        :return: None
        """
        try:
            requests.get(url, timeout=1)
            logger.info('Check the Internet connection.')
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
        ) as error:
            raise SystemExit(f'Error: {error}. URL {url} is unreachable.')
        else:
            logger.info('Connection established.')

    @staticmethod
    def check_response_status_code(response, logger):
        """
        Check if the response status code is 200: OK
        :param response: dict
        :param logger: logger
        :return: None
        """
        if response.get('status', '') != 200:
            raise Exception(f'Bad response status code {str(response.status)}')

        logger.info('The response status code is 200: OK.')

    def get_the_response(self, url, logger):
        """
        Get the response fro the url.
        :param url: str
        :param logger: logger
        :return: dict response
        """
        try:
            response = feedparser.parse(url)
            self.check_response_status_code(response, logger)
            logger.info(f'Getting the response from the URL: {url}.')
        except AttributeError:
            raise InvalidURL("Please, check the URL.")
        else:
            logger.info('Valid URL')
            return response

    def check_news_collection(self, news, logger):
        """
        Check news_collection is not empty
        """
        if not news:
            raise FeedError("Link doesn't contain any news.")
        else:
            logger.info("News was collected successfully.")

    def check_limit_value(self, limit):
        """
        Check if received limit value is valid
        :param limit: int: user defined limit value from command line arguments
        :return: int: valid value of limit variable
        """

        # total amount of news received from the site
        total = len(self.news)

        if limit < 0:
            self.logger.info(f'Check if the received limit value = {limit} is valid.')
            raise ValueError(f'Limit value is outside the valid range: from 1 to {total}.')
        elif not limit or limit > total:
            limit = total
            self.logger.info(f"The 'limit' variable is assigned the total amount of received news {limit}.")
            return limit

        return limit

    def parse_feed(self):
        """
        Parse set amount of news from URL and write required news to the list of dictionaries
        :return: list of dictionaries with appropriate info
        """
        img_link, img_title = None, None
        store_news = []

        self.logger.info('Extract the required data from the separated news '
                         'and fill the dictionaries with required data.')

        for info in self.news[:self.limit]:
            info_title = html.unescape(info.title)
            info_link = info.link
            info_date = info.published
            info_description = info.description

            # Pulling data out of HTML part
            soup = BeautifulSoup(info_description, features="html.parser")

            if soup.img:
                img_link = soup.img.get('src', '')
                img_title = html.unescape(soup.img.get('title', ''))

            info_text = html.unescape(soup.text)

            store_news.append({
                "title": info_title,
                "link": info_link,
                "date": info_date,
                "img_title": img_title,
                "img_link": img_link,
                "text": info_text,
            })
        return store_news

    def output_txt_news(self):
        """
        Fill template with required data
        """
        self.logger.info('Load the template.')

        directory = path.abspath(path.dirname(__file__))
        file_loader = FileSystemLoader((directory + '/templates/'), followlinks=True)
        env = Environment(loader=file_loader)
        template = env.get_template('template.txt')

        self.logger.info('Fill the template with relevant data.')

        output = template.render(feed_name=self.feed_name, all_news=self.all_news[:self.limit])

        print(output)
