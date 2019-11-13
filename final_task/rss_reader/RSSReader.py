import datetime
import json
import feedparser
import logging
import sys
from bs4 import BeautifulSoup
from RSSReaderException import RSSReaderException


class RSSReader:

    def __init__(self, url, is_verbose=False):
        self.url = url
        self.is_verbose = is_verbose
        self.is_json = False
        self.limit = None
        logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s', stream=sys.stdout, level=logging.ERROR)
        self.logger = logging.getLogger(__name__)
        if is_verbose:
            self.logger.setLevel(level=logging.INFO)

    def url_parsing(self):
        parsed_url = feedparser.parse(self.url)
        if parsed_url.status != 200:  # URL-access check
            self.logger.error("Can't load RSS feed.")
            raise RSSReaderException('RSS-reader failed. Status: {}.'.format(parsed_url.status))
        else:
            self.logger.info('RSS parsed successfully')
            return parsed_url

    def information_about_site(self, parsed_url):
        """Function which make dictionary with data of website"""
        date = parsed_url.get('updated', datetime.datetime.now())
        return {
            'Feed': parsed_url['feed']['title'],
            'Updated': date,
            'Version': parsed_url['version'],
        }

    def make_news_data(self, news):
        """
        Function which parsed HTML summary of news and make dictionary with all the necessary news data.
        :return dictionary
        """
        print(news)
        if 'summary' in news:
            bs = BeautifulSoup(news['summary'], 'html.parser')
            img = bs.find_all('img')
            image_data = 'No image'
            if img:
                image_data = '{}\nSource of image: {}'.format(img[0].get('alt', ""), img[0]['src'])
            summary = bs.get_text()
        else:
            summary = news['title']
            image_data = 'No image'
        news_summary = {
            'Title': news['title'],
            'Date': news['published'] if 'published' in news else news['updated'],
            'Link': news['link'],
            'Summary': summary,
            'Image': image_data,
        }
        return news_summary

    def news_data_collection(self, parsed_url):
        """Function that collects data from all news by calling make_news_data.
        :return string of dictionaries
        """
        all_information_about_news = parsed_url['entries']
        # amount_of_news = len(parsed_url.entries)
        all_news = []
        self.logger.info('News gathering')
        for news in all_information_about_news[:self.limit]:
            try:  # Exception when news is failed
                dictionary_of_news_data = self.make_news_data(news)
            except Exception as ex:
                self.logger.error("Error processing news: {} {}".format(type(ex), ex))
            else:
                all_news.append(dictionary_of_news_data)  # make list of dictionaries of news data for optional output
        return all_news

    def parse_to_json(self, dictionary):
        return json.dumps(dictionary, indent=4)

    def output(self, about_website, all_news):
        """Function which print information about site and a set of news."""
        for key, value in about_website.items():
            print('\n', key, ': ', value)
        for number_of_news in all_news:
            print("--------------------------------------------------------")
            for key, value in number_of_news.items():
                print(key, ': ', value)

    def output_json(self, about_website, all_news):
        print(self.parse_to_json([about_website] + all_news))

    def get_news(self):
        """Get news!"""
        self.logger.info('Start parsing')
        try:
            parsed_url = self.url_parsing()
            about_website = self.information_about_site(parsed_url)
        except Exception as ex:  # for any exception after website parsing
            self.logger.error("Error reading site data: {}, {}".format(type(ex), ex))
            return
        string_of_news_dictionaries = self.news_data_collection(parsed_url)
        if self.is_json:
            self.logger.info('Convert to JSON-format')
            self.output_json(about_website, string_of_news_dictionaries)
        else:
            self.logger.info('Output news')
            self.output(about_website, string_of_news_dictionaries)
