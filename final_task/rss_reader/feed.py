import logging
from string_operations import *
from pprint import pprint
import article


class Feed:
    """Feed class, contain feed info and list of articles """
    def __init__(self, parsed, number_of_articles):
        """create feed with fixed number of articles """
        logging.info('Started creting feed')
        self.feed_name = make_string_readable(parsed.feed.title)
        self.link = parsed.feed.link
        articles_list = []
        for i in range(number_of_articles):
            logging.info('  Started creating Article %s', i + 1)
            articles_list.append(article.Article(parsed.entries[i]))
            logging.info('  Finished creating Article %s', i + 1)
        self.articles = articles_list

    def print_readable_feed(self):
        """print feed to stdout in readable format"""
        logging.info('Started printing feed')
        print('.' * 79)
        print('\n\n%s\n\n', self.feed_name) 
        print(self.link, '[1]')
        for i, article_ in enumerate(self.articles):
            logging.info('  Started printing article %s', i+1)
            article_.print_readable_article()
            logging.info('  Finished printing article %s', i+1)
        logging.info('Finished printing feed')

    def print_json_feed(self):
        """print feed to stdout in json"""
        json = {}
        for i, article_ in enumerate(self.articles):
            name = "Article {}".format(i + 1)
            json[name] = article_.make_article_json()
        json['Feed'] = self.feed_name
        json['Link'] = self.link
        pprint(json)
