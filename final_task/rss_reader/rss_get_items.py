from bs4 import BeautifulSoup
import urllib.request as urlib2
import urllib.error as URLError
import logging as log

def rss_get_items(url):
    request =  urlib2.Request(url)
    try:
        response = urlib2.urlopen(request)
        except [urlib2.URLError, e]:
            log.info('URLError, pls try other one')
    soup = BeautifulSoup(response)

    for item_node in soup.find_all('item'):
        item = {}
        for subitem_node in item_node.findChildren():
            key = subitem_node.name
            value = subitem_node.text
            item[key] = value
    yield item