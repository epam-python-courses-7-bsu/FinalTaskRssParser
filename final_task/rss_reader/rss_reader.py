import sys
import requests
import argparse
import json
import logging
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
    logging.info("Getting feed from " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        channel = soup.find('channel')
    except requests.exceptions.ConnectionError:
        log.error("Wrong URL")
        print("Wrong URL: " + url)
        sys.exit()
    return channel


def collect_news(items, limit) -> list:
    """Sorts the components of the news into dictionaries and adds them into a list"""
    log.info("Collecting news...")
    news = []
    for item in items:
        try:
            news_item = {}
            news_item['title'] = item.title.text.replace("&#39;", "\'")
            news_item['date'] = item.pubDate.text
            soup = BeautifulSoup(item.description.text, 'lxml')
            news_item['description'] = soup.text.replace("&#39;", "\'")
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
            log.info("The limit of " + str(limit) + "pieces of news reached")
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
    log.info("Converting to JSON...")
    print(json.dumps(news, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))


def args_parse():
    log.info("Parsing arguments...")
    parser = argparse.ArgumentParser(description="RSS")
    parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=999, help='Limit news topics if this parameter provided')
    return parser.parse_args()


if __name__ == '__main__':
    log.info("Main")
    args = args_parse()
    if args.version:
        log.info("Version " + str(args.version))
        print("Version is 1.2")
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    if args.limit:
        limit = args.limit
        log.info("Limit = " + str(limit))
    if args.source:
        channel = find_channel(args.source)
        items = find_news(args.source)
        news = collect_news(items, limit)
        print_news(news, channel)
        if args.json:
            json_convert(news)
