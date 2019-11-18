import datetime
import logging as log
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
from collections import defaultdict


def get_items(url: str):
    request = urllib.request.Request(url)
    try:
        soup_xml = BeautifulSoup(
            urllib.request.urlopen(request),
            "xml"
        )
    except (urllib.error.URLError, KeyError):
        log.info('URLError, pls try other one')
    else:
        log.info('Connect to website is fine')
        items = []
        xml_items = list(soup_xml.find_all('item'))
        for rss_node_xml in xml_items:
            item_xml = defaultdict(list)
            for node in rss_node_xml.findChildren():
                key = node.name
                value = node.text
                if key == "content":
                    item_xml[key].append(node.attrs['url'])
                else:
                    item_xml[key] = value
            items.append(item_xml)

        return items


def description(description_element: str) -> str:
    """ Try to delete all html in description """
    return BeautifulSoup(description_element, "html.parser").getText()


def pubdate(pub_date: str) -> str:
    """reformat publication date"""
    if pubdate:
        # pub_date = datetime.datetime(*map(int, pub_date.split(' ')[1:5]))
        # new_pub_date = datetime.datetime.strftime(pub_date, '%Y-%m-%d')
        return pub_date
    return pub_date


def get_json(item):
    json = {}
    item.update(json)
    print(json)
