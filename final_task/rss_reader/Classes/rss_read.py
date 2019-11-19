import feedparser
from output_functions import getting_full_info, getting_pack_of_news, converting_to_json, \
    writing_to_file, getting_from_database_to_pack
from pdf_and_html_converting import converting_to_pdf, converting_to_html, pdf_path, html_path
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
        4. Do parse method
        5. If there are some arguments from console - work with them
        """
        try:
            logging.info("Trying to get page from feedparser!")
            the_feed = feedparser.parse(self.feed_url)
            logging.info("Got it (the page)!")
            if the_feed.get('bozo') == 1:
                if '--date' in self.list_of_args:
                    if '--to-pdf' in self.list_of_args:
                        path_pdf = pdf_path(self.list_of_args)
                        pack_news = self.news_for_date()
                        converting_to_pdf(path_pdf, pack_news)
                    elif '--to-html' in self.list_of_args:
                        path_html = html_path(self.list_of_args)
                        pack_news = self.news_for_date()
                        converting_to_pdf(path_html, pack_news)
                    else:
                        logging.info("Getting news for date!")
                        news = self.news_for_date()
                        getting_full_info(the_feed, news, self.list_of_args)
                        logging.info("Got news for date!")
                else:
                    logging.info("Got some problems due to connection!")
        except ConnectionError:
            logging.critical("CONNECTION ERROR, HELP!")
            print("You have some connection problems!")
            if '--date' in self.list_of_args:
                if '--to-pdf' in self.list_of_args:
                    path_pdf = pdf_path(self.list_of_args)
                    pack_news = self.news_for_date()
                    converting_to_pdf(path_pdf, pack_news)
                elif '--to-html' in self.list_of_args:
                    path_html = html_path(self.list_of_args)
                    pack_news = self.news_for_date()
                    converting_to_html(path_html, pack_news)
                else:
                    self.news_for_date()

        logging.info("Getting pack of news!")
        pack_of_news, pack_of_news_for_db = getting_pack_of_news(the_feed, self.feed_url, self.number)
        logging.info("Got pack of news!")
        if '--json' in self.list_of_args:
            print("\nJSON VIEW OF NEWS:", converting_to_json(pack_of_news, the_feed))
        logging.info("Writing news from source and DB to file!")
        writing_to_file(pack_of_news, pack_of_news_for_db, 'news_cache.txt')
        logging.info("News are in the file!")
        if '--to-html' in self.list_of_args:
            path_html = html_path(self.list_of_args)
            if '--date' in self.list_of_args:
                pack = self.news_for_date()
                converting_to_html(path_html, pack)
            else:
                converting_to_html(path_html, pack_of_news)
        if '--to-pdf' in self.list_of_args:
            path_pdf = pdf_path(self.list_of_args)
            if '--date' in self.list_of_args:
                pack = self.news_for_date()
                converting_to_pdf(path_pdf, pack)
            else:
                converting_to_pdf(path_pdf, pack_of_news)

        else:
            if '--date' in self.list_of_args:
                logging.info("Getting full info!")
                getting_full_info(the_feed, self.news_for_date(), self.list_of_args)
                logging.info("Got full info!")
            else:
                logging.info("Getting full info!")
                getting_full_info(the_feed, pack_of_news, self.list_of_args)
                logging.info("Got full info!")

    def news_for_date(self):
        """
        Finding news by date and rss
        If your rss and date are correct we append the novelty to the pack_of_news_needed
        If not we continue our searching
        """
        try:
            news_for_date_needed = []
            date_needed = self.list_of_args[self.list_of_args.index('--date') + 1]
            pack_of_db_news = getting_from_database_to_pack()
            if '--limit' in self.list_of_args:
                cycle_counter = 0
                number_of_news_found = 0
                while cycle_counter != len(pack_of_db_news):
                    if str(pack_of_db_news[cycle_counter].date_corrected) == date_needed and \
                            self.feed_url == pack_of_db_news[cycle_counter].main_source:
                        news_for_date_needed.append(pack_of_db_news[cycle_counter])
                        number_of_news_found += 1
                    if number_of_news_found == self.number:
                        break
                    cycle_counter += 1
            else:
                for item in pack_of_db_news:
                    if str(item.date_corrected) == date_needed and \
                            self.feed_url == item.main_source:
                        news_for_date_needed.append(item)
            if self.feed_url is None:
                counter = 0
                number_of_news_f = 0
                while counter != len(pack_of_db_news):
                    if str(pack_of_db_news[counter].date_corrected) == date_needed:
                        pack_of_db_news[counter].number_of_novelty = number_of_news_f + 1
                        news_for_date_needed.append(pack_of_db_news[counter])
                        number_of_news_f += 1
                    counter += 1
                    if '--limit' in self.list_of_args:
                        if number_of_news_f == self.number:
                            break
            if not news_for_date_needed:
                if '--limit' in self.list_of_args:
                    print("No news have been found for this date with your limits!")
                elif 'source' in self.list_of_args:
                    print("No news have been found for your source")
                else:
                    print("No news have been found for this date!")
            if '--json' in self.list_of_args:
                print("\nJSON VIEW OF NEWS:", converting_to_json(news_for_date_needed))
            return news_for_date_needed
        except IndexError:
            print("You forgot to enter date in format %Y%m%d")

