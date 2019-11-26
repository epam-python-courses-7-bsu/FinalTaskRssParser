#!/usr/bin/env python3.8
"""
Module for parsing news from the given link, extracting required info from it
and filling the list with dictionaries containing received data
"""

import html

from bs4 import BeautifulSoup
import feedparser

from logger import LOGGER
from validator import check_limit_value, check_news_collection


class RSSparser:
    """
    Parsed the RSS news from received link, extracts required amount of news

    Parameters:
        cmd_args: dict: parsed arguments out of sys.argv

    Returns:
        all_news: list of dictionaries with extracted info of required amount of parsed news
    """

    def __init__(self, cmd_args):
        self.url = cmd_args.source
        self.limit = cmd_args.limit
        check_limit_value(self.limit)

        LOGGER.info(f'Get RSS_url {self.url} and value = {self.limit} (limits amount of output news)')

        self.response = self.get_the_response()

        # Extract the news-site name converting it to the unicode
        self.feed_name = html.unescape(self.response.feed.get('title', ''))

        LOGGER.info('Trying to separate news from the URL.')

        # Extract all news separately in one list
        self.news = self.response.entries
        check_news_collection(self.news)

    def get_the_response(self):
        """
        Get the response from the url.
        """
        response = feedparser.parse(self.url)
        LOGGER.info(f'Getting the response from the URL: {self.url}.')
        return response

    def parse_feed(self):
        """
        Parse set amount of news from URL and write required news to the list of dictionaries
        :return: list of dictionaries with appropriate info
        """
        all_news = []

        LOGGER.info('Extract the required data from the separated news and fill the dictionaries with required data.')

        limit = self.limit or len(self.news)

        for info in self.news[:limit]:
            img_link, img_title = [], []
            info_title = html.unescape(info.title)
            info_link = info.link
            info_date = info.published
            info_description = info.description

            # Pulling data out of HTML part
            soup = BeautifulSoup(info_description, features="html.parser")

            img_tag_list = soup.find_all('img')
            if img_tag_list:
                for link in img_tag_list:
                    img_link.append(link.get('src'))
                    img_title.append(html.unescape(link.get('title', '')))

            info_text = html.unescape(soup.text).rstrip()

            all_news.append({
                "feed_title": self.feed_name,
                "feed_url": self.url,
                "title": info_title,
                "link": info_link,
                "date": info_date,
                "img_title": img_title,
                "img_link": img_link,
                "text": info_text,
            })
        return all_news
