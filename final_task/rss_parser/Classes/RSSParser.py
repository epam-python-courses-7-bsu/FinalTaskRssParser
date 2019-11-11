import feedparser
from final_task.rss_parser.Output_functions import getting_full_info, getting_pack_of_news, converting_to_json
import logging

class RSSParser:
    """
    class RSSParser has 3 parameters and it calls function parse when created
    """
    def __init__(self, param_url, num_of_news=None, list_of_args=None):
        self.feed_url = param_url
        self.number = num_of_news
        self.list_of_args = list_of_args
        self.parse()



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
                logging.info("Got some problems due to connection!")
                raise ConnectionError
        except ConnectionError:
            logging.critical("CONNECTION ERROR, HELP!")
            print("You have some connection problems!")

        # try:
        logging.info("Getting pack of news!")
        pack_of_news = getting_pack_of_news(the_feed, self.number)
        logging.info("Got pack of news!")
        logging.info("Getting full info!")
        getting_full_info(pack_of_news)
        logging.info("Got full info!")
        if '--json' in self.list_of_args:
            print("\nJSON VIEW OF NEWS:", converting_to_json(the_feed, pack_of_news, self.number))
        if '--version' in self.list_of_args:
            print("\nVERSION: 1.0")

        # except IndexError:
        #     print("You want to get more news than exist!")
        #     print("You can get only {0} news.".format(len(the_feed.entries)))