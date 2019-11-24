import datetime
import feedparser
import logging
from bs4 import BeautifulSoup
from RSSReaderException import RSSReaderException
from NewsCache import NewsCache
from unidecode import unidecode
from output import get_output_function

CACHE_FILE_NAME = "Cache file.json"


class RSSReader:

    def __init__(self, date, url, limit, is_json, is_pdf, is_epub):
        self.cache = NewsCache(CACHE_FILE_NAME)
        self.date = date
        self.url = url
        self.is_json = is_json
        self.limit = limit
        self.is_pdf = is_pdf
        self.is_epub = is_epub
        self.logger = logging.getLogger(__name__)

    def url_parsing(self):
        parsed_url = feedparser.parse(self.url)
        if parsed_url.status != 200:  # URL-access check
            self.logger.error("Can't load RSS feed.")
            raise RSSReaderException('RSS-reader failed. Status: {}.'.format(parsed_url.status))
        else:
            self.logger.info('RSS parsed successfully!')
            return parsed_url

    def information_about_site(self, parsed_url):
        """Function which make dictionary with data of website"""
        date = parsed_url.get('updated', str(datetime.datetime.now()))
        return {
            'Feed': unidecode(parsed_url['feed']['title']),
            'Updated': date,
            'Version': unidecode(parsed_url['version']),
        }

    def make_news_data(self, news):
        """
        Function which parsed HTML summary of news and make dictionary with all the necessary news data.
        :return dictionary
        """
        image_link = 'No image'
        if 'summary' in news:
            # convert_to_epub(news['summary'])
            bs = BeautifulSoup(news['summary'], 'html.parser')
            img = bs.find_all('img')
            if img:
                image_description = unidecode(img[0].get('alt', 'no description'))
                image_link = img[0].get('src')
                img[0].replaceWith(f' [Image: {image_description}] ')
            summary = unidecode(str(bs.text))
        else:
            summary = news['title']
        date_info = news['published_parsed'] if 'published' in news else news['updated_parsed']
        date_key = str("{}{}{}".format(date_info.tm_year, date_info.tm_mon, date_info.tm_mday))
        news_summary = {
            'Title': unidecode(news['title']),
            'Date': news['published'] if 'published' in news else news['updated'],
            'Link': news['link'],
            'Summary': summary,
            'Source of image': image_link,
            'Date key': date_key
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

    def get_news(self):
        """Get news!"""
        if self.date is None:
            if self.url is None:
                self.logger.error("URL is not provided.")
                return
            self.logger.info('Start parsing...')
            try:
                parsed_url = self.url_parsing()
                about_website = self.information_about_site(parsed_url)
            except Exception as ex:  # for any exception after website parsing
                self.logger.error("Error reading site data: {}, {}.".format(type(ex), ex))
                return
            string_of_news_dictionaries = self.news_data_collection(parsed_url)
            self.cache.caching(string_of_news_dictionaries, self.url)
        else:
            string_of_news_dictionaries = self.cache.returning(self.date, self.url)[:self.limit]
            about_website = None
        if not string_of_news_dictionaries:
            self.logger.error('There is no news.')
            return
        if self.is_json:
            converter = 'json'
        elif self.is_pdf:
            converter = 'pdf'
        elif self.is_epub:
            converter = 'epub'
        else:
            self.logger.info('Output news')
            converter = 'text'
        output = get_output_function(converter)
        output(self.logger, string_of_news_dictionaries, about_website)
