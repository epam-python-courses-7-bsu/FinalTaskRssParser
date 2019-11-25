import json
import os.path
import logging


class NewsCache:
    """Class which create json-file with cached news,
    saved all fresh news and return them with certain date
    and from certain url-address if such url will be introduced."""

    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.file_name = file_name
        self.logger.info("Check for cache file...")
        if os.path.isfile(file_name):
            try:
                with open(file_name, "r") as json_file:
                    self.cache_news = json.load(json_file)
                    self.logger.info("Reading cache file...")
            except Exception as ex:
                self.logger.error("Error reading file: {} {}".format(type(ex), ex))
                self.cache_news = {}
        else:
            self.logger.warning("Warning! Caching file is not found!")
            self.cache_news = {}

    def caching(self, all_news, url):
        """Function which create JSON-file
        and save news."""
        for dictionary in all_news:
            date_in_news = dictionary.pop('Date key')
            title = dictionary['Title']
            self.cache_news.setdefault(date_in_news, {}).setdefault(url, {}).setdefault(title, dictionary)
        with open(self.file_name, "w") as file_to_write:
            self.logger.info("News caching...")
            file_to_write.write(json.dumps(self.cache_news))

    def returning(self, desired_date, desired_url=None):
        """Function which return news from cache-file with certain date
        and from certain url-address if such url will be introduced."""
        self.logger.info('News search in cache...')
        caching_news_list = []
        if desired_url is not None:
            caching_news_list = list(self.cache_news.get(desired_date, {}).get(desired_url, {}).values())
        else:
            answer = self.cache_news.get(desired_date, {})
            for title in answer.values():
                caching_news_list += title.values()
        return caching_news_list
