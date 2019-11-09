from bs4 import BeautifulSoup
import feedparser
import json
import re
import logging

# url = "https://news.yahoo.com/rss"
# url1 = "https://news.google.com/rss"
# url2 = "https://www.theguardian.com/world/rss"

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', 
                    level = logging.DEBUG, filename = u'parser.log')

def getEntries(url, json, verbose, limit):

    channel = feedparser.parse(url)

    print("Feed: ", channel.feed.title, '\n')

    limit = limit or len(channel.entries)

    for item in (channel.entries):

        if (limit > 0):
            loggingItems(item)

            if (json):
                print(getJSON(item))

            else:
                print("Title: ", item.title)
                print("Date: ", item.published)
                print("Link: ", item.link, '\n')
                print("Description: ", getDescription(item.description), '\n')
                print("Links:", "\n[1]: ", item.link, "(link)\n[2]: ",
                item.media_content[0]['url'],'\n')
            
        limit -= 1

def getDescription(item):
    return BeautifulSoup(item, features="html.parser").getText()

def printLogs():
    with open('parser.log', 'r') as f:
        for line in f:
            print(line)

def loggingItems(item):
    logging.debug("Title: " + str(item.title))
    logging.debug("Date: " + str(item.published))
    logging.debug("Link: " + str(item.link) + '\n')
    # logging.debug("Description: ", item.description[1], '\n')
    logging.debug("Links:"+"\n[1]: " + str(item.link) +
                "(link)\n[2]: " + str(item.media_content[0]['url'])+'\n')


def getJSON(item):

    return json.dumps({
        'Title: ': item.title,
        'Date: ' : item.published,
        'Link: ' : item.link,
        #'Description: ' : item
    })



