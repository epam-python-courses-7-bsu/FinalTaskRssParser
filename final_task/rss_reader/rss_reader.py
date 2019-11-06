import socket
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
    while True:
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content, features="xml")
            items = soup.findAll('item')
            log.info(str(len(items))+" pieces of news have been found")
        except requests.exceptions.MissingSchema:
            log.error("Wrong URL")
            print("Wrong URL: " + url)
            print("Try to input a correct URL: ")
            url = input()
        except requests.exceptions.ConnectionError:
            log.error("Can't connect to the " + url)
            print("Can't connect to the " + url)
            print("Try to input a different URL: ")
            url = input()
        else:
            break
    return items


def collect_news(items, limit) -> list:
    """Sorts the components of the news into dictionaries and adds them into a list"""
    news = []
    for item in items:
        try:
            news_item = {}
            news_item['title'] = item.title.text
            news_item['description'] = item.description.text
            news_item['link'] = item.link.text
            if item.thumbnail != None:
                news_item['image'] = item.thumbnail['url']
            elif item.content != None:
                news_item['image'] = item.content['url']
            else:
                news_item['image'] = item.enclosure['url']
        except TypeError:
            log.error("Could not load an image")
            news_item['image'] = "No image"
        news.append(news_item)
        if len(news) == limit:
            break
    return news


def print_news(list_of_news):
    for item in list_of_news:
        print("Title: " + item['title'])
        print("Description: " + item['description'])
        print("Image: " + item['image'])
        print("Link: " + item['link'])
        print('------------------')


def json_convert(news):
    """Converts the news into JSON format"""
    with open("README.md", "w") as write_file:
        json.dump(news, write_file)


if __name__ == '__main__':
    
    while True:
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
        else:
            break

if args.version:
    print("Version is 1.0")
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

if args.limit:
    if args.limit > 0:
        limit = args.limit
        else:
            limit = 5

items = find_news(args.source)
news = collect_news(items, limit)
print_news(news)

if args.json:
    json_convert(news)






