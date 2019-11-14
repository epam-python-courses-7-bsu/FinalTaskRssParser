import logging
from clean_output import clean_title


logging.basicConfig(filename="loggs.log", level=logging.DEBUG)


def logg(article):
    logging.debug("Title: " + clear_title(article['title']))
    logging.debug("Date: " + article['published'])
    logging.debug("Link: " + article['link'])
    logging.debug("Description: " + article['summary'] + '\n')

def logg_json(json_format):
    logging.debug("Json: " + json_format)