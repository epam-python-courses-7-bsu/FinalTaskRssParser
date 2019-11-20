import re
import feedparser
import socket
import logging
from dateutil import parser as date_parser
import html
from personal_exceptions import *


def ckeck_internet():
    """
    Checks Internet connetction
    """
    try:
        logging.info("checking Internet connection")
        socket.setdefaulttimeout(5)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        s.close()
        logging.info('Internet on.')
        return True
    except Exception as e:
        logging.error("Internet off.")
        return False


def get_new_description(summary_str):
    """
    :param summary_str: Summary string from parsing RSS
    :return: New description
    Extract new description from summary string
    """
    pattern = re.compile(r'<.*?>')
    return pattern.sub('', summary_str)


def get_image_description(summary_str):
    """
       :param summary_str: Summary string from parsing RSS
       :return: Image description
       Extract image description from summary string
       """
    return summary_str[summary_str.find('alt') + 5::].split('"')[0]


def get_news_list(source, limit):
    """
    :param source - RSS URL:
    :param limit - Limit of viewing news:
    :return - RSS display list:
    Function parsing the rss received from source
    into a list of news which will then be used for printing or parsing into JSON
    """
    logging.info('Creating news list')
    if not ckeck_internet():
        raise NoInternet
    logging.info('Getting and parsing RSS')
    parsed_rss = feedparser.parse(source)
    if parsed_rss['bozo'] == 1:
        raise IncorrectURL
    if limit:
        limit = min(limit, len(parsed_rss['entries']))
    else:
        limit = len(parsed_rss['entries'])
    news_list = []
    for index in range(limit):
        news_list.append({'Feed':
                              html.unescape(parsed_rss['feed']['title']),
                          'Title':
                              html.unescape(parsed_rss['entries'][index]['title']),
                          'Date':
                              str(date_parser.parse(parsed_rss['entries'][index]['published'])),
                          'Link':
                              parsed_rss['entries'][index]['link'],
                          'Image description':
                              html.unescape(get_image_description(parsed_rss['entries'][index]['summary'])),
                          'New description':
                              html.unescape(get_new_description(parsed_rss['entries'][index]['summary'])),
                          'Image links':
                              [content['url'] for content in parsed_rss['entries'][index]['media_content']]})
    return news_list
