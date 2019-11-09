import socket
import sys
import requests
import argparse
import json
import logging
import pycodestyle
from bs4 import BeautifulSoup


log = logging.getLogger("Log")


def find_news(url):
    """Parses news"""
    logging.info("Searching for news on " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll('item')
        log.info(str(len(items)) + " pieces of news have been found")
    except requests.exceptions.MissingSchema:
        log.error("Wrong URL")
        print("Wrong URL: " + url)
        sys.exit()
    except requests.exceptions.ConnectionError:
        log.error("Can't connect to the " + url)
        print("Can't connect to the " + url)
        sys.exit()
    return items


def find_channel(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features="xml")
    channel = soup.find('channel')
    return channel


def collect_news(items, limit) -> list:
    """Sorts the components of the news into dictionaries and adds them into a list"""
    news = []
    for item in items:
        try:
            news_item = {}
            news_item['title'] = item.title.text
            news_item['date'] = item.pubDate.text
            soup = BeautifulSoup(item.description.text,'lxml')
            news_item['description'] = soup.text
            news_item['link'] = item.link.text
            if item.thumbnail:
                news_item['image'] = item.thumbnail['url']
            elif item.content:
                news_item['image'] = item.content['url']
            else:
                news_item['image'] = item.enclosure['url']
            if soup.find('img'):
                news_item['alt'] = soup.find('img')['alt']
            elif item.find('media:text'):
                soup = BeautifulSoup(item.find('media:text').text, 'lxml')
                news_item['alt'] = soup.find('img')['alt']
            else:
                news_item['alt'] = None
        except TypeError:
            log.error("Could not load an image")
            news_item['image'] = "No image"
        except AttributeError:
            log.error("Probably no description")
            news_item['description'] = "No description"
        news.append(news_item)
        if len(news) == limit:
            break
    return news


def print_news(list_of_news, channel):
    print("Feed: " + channel.title.text + '\n\n')
    for item in list_of_news:
        print("Title: " + item['title'])
        print("Date: " + item['date'])
        print("Description: " + item['description'])
        print("Image: " + item['image'])
        if item['alt']:
            print("Alt: " + item['alt'])
        print("Link: " + item['link'])
        print('------------------')


def json_convert(news):
    """Converts the news into JSON format"""
    with open("JSON.json", "w") as write_file:
        json.dump(news, write_file)


if __name__ == '__main__':
    
    try:
        parser = argparse.ArgumentParser(description="RSS")
        parser.add_argument('source', type=str, help='RSS URL')
        parser.add_argument('--version', action='store_true', help='Print version info')
        parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
        parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
        parser.add_argument('--limit', type=int, default=999, help='Limit news topics if this parameter provided')
        args = parser.parse_args()
    except SyntaxError:
        print("Wrong syntax in args")
        sys.exit()
    
    if args.version:
        print("Version is 1.1")
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    if args.limit:
        if args.limit > 0:
            limit = args.limit
        else:
            limit = 5
    channel = find_channel(args.source)
    items = find_news(args.source)
    news = collect_news(items, limit)
    print_news(news, channel)

if args.json:
    json_convert(news)
