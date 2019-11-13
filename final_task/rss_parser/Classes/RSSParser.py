import feedparser
from Output_functions import getting_full_info, getting_pack_of_news, converting_to_json, \
    writing_to_file, getting_from_json_to_pack
import logging


class RSSParser:
    """
    class RSSParser has 3 parameters and it calls function parse when created
    """

    def __init__(self, param_url, num_of_news=None, list_of_args=None):
        self.feed_url = param_url
        self.number = num_of_news
        self.list_of_args = list_of_args

    def parse(self):
        """
        1. Use feedparser to get the page
        2. If we have some problems with connection - raise ConnectionError
        3. Handle Exception without showing a traceback
        :return:
        """
        try:
            logging.info("Trying to get page from feedparser!")
            the_feed = feedparser.parse(self.feed_url)
            logging.info("Got it (the page)!")
            if the_feed.get('bozo') == 1:
                if '--date' in self.list_of_args:
                    self.news_for_date()
                else:
                    logging.info("Got some problems due to connection!")
                    raise ConnectionError
        except ConnectionError:
            logging.critical("CONNECTION ERROR, HELP!")
            print("You have some connection problems!")
            if '--date' in self.list_of_args:
                self.news_for_date()

        logging.info("Getting pack of news!")
        pack_of_news = getting_pack_of_news(the_feed, self.feed_url, self.number)
        logging.info("Got pack of news!")
        if '--json' in self.list_of_args:
            print("\nJSON VIEW OF NEWS:", converting_to_json(the_feed, pack_of_news, self.number))

        writing_to_file(pack_of_news, 'News_cache.txt')

        logging.info("Getting full info!")
        getting_full_info(pack_of_news)
        logging.info("Got full info!")

    def news_for_date(self):
        """
        Finding news by date and rss
        If your rss and date are correct we append the novelty to the pack_of_news_needed
        If not we continue our searching
        :return:
        """
        try:
            news_for_date_needed = []
            date_needed = self.list_of_args[self.list_of_args.index('--date') + 1]
            pack_of_json_news = getting_from_json_to_pack('News_cache_json.txt')
            if '--limit' in self.list_of_args:
                cycle_counter = 0
                number_of_news_found = 0
                while cycle_counter != len(pack_of_json_news):
                    if pack_of_json_news[cycle_counter].date_corrected == date_needed and \
                            self.feed_url == pack_of_json_news[cycle_counter].main_source:
                        news_for_date_needed.append(pack_of_json_news[cycle_counter])
                        number_of_news_found += 1
                    if number_of_news_found == self.number:
                        break
                    cycle_counter += 1
            else:
                for item in pack_of_json_news:
                    if item.date_corrected == date_needed and \
                            self.feed_url == item.main_source:
                        print("THE NOVELTY YOU NEED")
                        news_for_date_needed.append(item)
            if not news_for_date_needed:
                if '--limit' in self.list_of_args:
                    print("No news have been found for this date with your limits!")
                elif 'source' in self.list_of_args:
                    print("No news have been found for your source")
                else:
                    print("No news have been found for this date!")
            getting_full_info(news_for_date_needed)
        except IndexError:
            print("You forgot to enter date in format %Y%m%d")
