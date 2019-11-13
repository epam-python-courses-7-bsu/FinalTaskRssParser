import json
import jsonpickle
from classes.logger import logger


class rss_feed:
    '''
    Contatins RSS channel title, description, link and list of news
    Contatins method for parsing class to json via jsonpickle module
    '''
    def __init__(self, title, description, link, news_list):
        logger.log('INIT RSS FEED CLASS')
        self.news_list = news_list
        self.title = title  
        self.description = description
        self.link = link
    
    def print_feed(self):
        print()
        print(' '*36 + self.title)
        print(' '*36 + '='*len(self.title))
        #This line do some math to align descrtiption and title
        print(' '*int(abs((36 + len(self.title)/2 - len(self.description)/2))) + self.description + '\n')
        print('='*120)
        for _, item in enumerate(self.news_list):
            print(item)
            print('='*120)
    
    def toJSON(self):
        '''
        Parses rss_feed class to JSON
        Method uses jsonpickle module because of using list of classes as field.
        load_backend() and set_encoder_options() loads standart json lib and set
        proper params to beautify json string
        '''
        logger.log('FORMATTING FEED TO JSON')
        jsonpickle.load_backend('json', 'dumps', 'loads')
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', indent=4, sort_keys=False)
        json_string = jsonpickle.encode(self, make_refs=False, unpicklable=False)
        logger.log('PRINTING JSON')
        print(json_string)
