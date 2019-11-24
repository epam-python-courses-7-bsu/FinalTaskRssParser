import logging as log
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
from collections import defaultdict

import check


def get_items(url: str):
    if check.internet_on:
        log.info("Start get items from url")
        request = urllib.request.Request(url)
        try:
            soup_xml = BeautifulSoup(
                urllib.request.urlopen(request),
                "xml"
            )
        except (urllib.error.URLError, KeyError):
            log.info("URLError, pls try other one")
        else:
            log.info("Connect to website is fine")
            items = []
            xml_items = list(soup_xml.find_all("item"))
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
            log.info("Successful parsing")
            return items
    else:
        log.info("There isn't internet connection")
        print("Check your internet connection or use database")


def description(description_element: str) -> str:
    """
        Try to delete all html in description
    """
    log.info("Try to delete all html in description")
    return BeautifulSoup(description_element, "html.parser").getText()


def pubdate(pub_date: str) -> str:
    """reformat publication date"""
    return pub_date
