import json

import jsonpickle

from classes.logger import logger


class RssFeed:
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
        result = '\n'
        result += ' '*36 + self.title + '\n'
        result += ' '*36 + '='*len(self.title) + '\n'
        
        #This line do some math to align descrtiption and title
        result +=' '*int(abs((36 + len(self.title)/2 - len(self.description)/2))) + self.description + '\n\n'
        result +='='*120 + '\n'
        for _, item in enumerate(self.news_list):
            result += str(item)  + '\n'
            result += '='*120 + '\n'
        print(result)
    
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
