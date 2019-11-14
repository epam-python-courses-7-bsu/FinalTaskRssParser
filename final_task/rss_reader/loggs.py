
import logging
from clean_output import delete_html, clean


logging.basicConfig(filename="loggs.log", level=logging.DEBUG)


def logg(article):
    logging.debug("Title: " + clean(article['title']))
    logging.debug("Date: " + article['published'])
    logging.debug("Link: " + article['link'])
    logging.debug("Description: " + clean(delete_html(article['summary'])) + '\n')

def logg_json(json_format):
    logging.debug("Json: " + json_format)