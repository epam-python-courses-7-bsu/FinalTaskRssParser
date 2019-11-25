import logging
from clean_output import delete_unnecessary_symbols


logging.basicConfig(filename="loggs.log", level=logging.DEBUG)


def logg(article):
    logging.debug("Title: " + delete_unnecessary_symbols(article['title']))
    logging.debug("Date: " + article['published'])
    logging.debug("Link: " + article['link'])
    logging.debug("Description: " + article['summary'] + '\n')

def logg_json(json_format):
    logging.debug("Json: " + json_format)