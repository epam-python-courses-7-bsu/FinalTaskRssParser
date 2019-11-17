import datetime
import logging as log
import urllib.error
import urllib.request
from bs4 import BeautifulSoup


def get_items(url):
    request = urllib.request.Request(url)
    item = {}
    try:
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, "html.parser")
    except (urllib.error.URLError, KeyError):
        log.info('URLError, pls try other one')
    else:
        log.info('Connect to website is fine')

    for item_node in soup.find_all('item'):
        for setitem_node in item_node.findChildren():
            key = setitem_node.name
            value = setitem_node.text
            item[key] = value
    return item


""" Try to delete all html in description """


def description(item):
    return BeautifulSoup(item, "html.parser").getText()


def pubdate(pub_date):
    pub_date = (pub_date.split(' ')[1:5])
    new_pub_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
    return new_pub_date


"""  Check if there is media content """


def media_content(item):
    media = ''
    if 'media_content' in item.keys():
        media = item.media_content[0]['url']
    elif 'media_thumbnail' in item.keys():
        media = item.media_thumbnail[0]['url']
    return media


def get_json(item):
    json = {}
    item.update(json)
    print(json)
