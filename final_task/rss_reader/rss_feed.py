import json
import logging
import re
import sys
from codecs import encode, decode

import jsonpickle
import requests
from colorama import Fore, Back, Style, init
from tinydb import Query, TinyDB, where

LOGGER = logging.getLogger('rss_logger')
init()


class RssFeed:
    '''
    Contatins RSS channel title, description, link and list of news
    Contatins method for parsing class to json via jsonpickle module
    '''
    def __init__(self, title, description, link, news_list):
        LOGGER.debug('INIT RSS FEED CLASS')
        self.news_list = news_list
        self.title = title
        self.description = description
        self.link = link

    def print_feed(self):
        result = '\n'
        result += ' '*36 + self.title + '\n'
        result += ' '*36 + Back.BLACK + '='*len(self.title) + Back.RESET + '\n'
        # This line do some math to align descrtiption and title
        result += ' '*int(abs((36 + len(self.title)/2 - len(self.description)/2))) + self.description + '\n\n'
        result += Back.RED + '='*120 + Back.RESET + '\n'
        for _, item in enumerate(self.news_list):
            result += str(item) + '\n'
            result += Back.RED + '='*120 + Back.RESET + '\n'
        print(result)

    def to_json(self):
        '''
        Parses rss_feed class to JSON
        Method uses jsonpickle module because of using list of classes as field.
        load_backend() and set_encoder_options() loads standart json lib and set
        proper params to beautify json string
        '''
        LOGGER.debug('FORMATTING FEED TO JSON')
        jsonpickle.load_backend('json', 'dumps', 'loads')
        jsonpickle.set_preferred_backend('json')
        # ensure_ascii = False to solve encoding problems
        jsonpickle.set_encoder_options('json', indent=4, sort_keys=False, ensure_ascii=False)
        json_string = jsonpickle.encode(self, make_refs=False, unpicklable=False)
        # Regex finds base64 string and replaces it for shorter output
        json_string = re.sub(r'(\"img\":\ )\"b\'.*?\'', r'\1"base64 image', json_string)
        # Unescaping
        json_string = decode(encode(json_string, 'latin-1', 'backslashreplace'), 'unicode-escape')
        LOGGER.debug('PRINTING JSON')
        print(json_string)

    def cache(self, cache_store):
        '''
        Using TinyDB for simple caching. Database stores RssItem class in
        json format.
        '''
        LOGGER.debug('INIT DATABASE')
        database = TinyDB(cache_store, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        LOGGER.debug('CACHING...')
        for _, news_item in enumerate(self.news_list):
            current_news = Query()
            # Checking if the news is already stored in database
            if not database.contains(current_news.link == news_item.link):
                database.insert(news_item.__dict__)
        LOGGER.debug('DONE!')
        database.close()

    def get_news_as_dicts(self, limit):
        news_list_dicts = []
        if limit is None or limit > len(self.news_list) or limit < 0:
            limit = len(self.news_list)
        self.news_list = self.news_list[:limit]
        for news_item in self.news_list:
            news_list_dicts.append(news_item.asdict())
        return news_list_dicts
