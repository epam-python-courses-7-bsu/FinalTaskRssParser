import requests
import argparse
import json
import logging
import socket
import bs4
from bs4 import BeautifulSoup


log = logging.getLogger("Log")


class CustomEx(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)


def is_connected() -> bool:
    log.info("Checking internet connection...")
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    raise CustomEx("No internet connection")


def find_news(url) -> bs4.element.ResultSet:
    """Parses news"""
    logging.info("Searching for news on " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll('item')
        log.info(str(len(items)) + " pieces of news have been found")
    except requests.exceptions.MissingSchema:
        log.error("Wrong URL")
        raise CustomEx("Wrong URL: " + url)
    except requests.exceptions.ConnectionError:
        log.error("Can't connect to the " + url)
        raise CustomEx("Can't connect to the " + url)
    return items


def find_channel(url) -> bs4.element.Tag:
    logging.info("Getting feed from " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        channel = soup.find('channel')
    except requests.exceptions.ConnectionError:
        log.error("Wrong URL")
        raise CustomEx("Wrong URL: " + url)
    return channel


def collect_news(items, limit) -> list:
    """Sorts the components of the news into dictionaries and adds them into a list"""
    log.info("Collecting news...")
    news = []
    for item in items:
        try:
            news_item = {}
            images = []
            alts = []
            news_item['title'] = item.title.text.replace("&#39;", "\'")
            news_item['date'] = item.pubDate.text
            soup = BeautifulSoup(item.description.text, 'lxml')
            news_item['description'] = soup.text.replace("&#39;", "\'")
            news_item['link'] = item.link.text
            if item.thumbnail:
                for img in item.findAll('thumbnail'):
                    images.append(img['url'])
            if item.content:
                for img in item.findAll('content'):
                    images.append(img['url'])
            if item.enclosure:
                for img in item.findAll('enclosure'):
                    images.append(img['url'])
            if len(images) == 0:
                news_item['image'] = None
            else:
                news_item['image'] = images
            if soup.find('img'):
                for alt in soup.findAll('img'):
                    alts.append(alt['alt'])
            if item.find('media:text'):
                log.info('media:text')
                soup = BeautifulSoup(item.find('media:text').text, 'lxml')
                for alt in soup:
                    alts.append(alt.find('img')['alt'])
            # if len(item.credit.text) > 0:
            #     log.info(item.credit.text)
            #     alts.append(item.credit.text)
            if len(alts) == 0:
                news_item['alt'] = None
            else:
                news_item['alt'] = alts
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
        if item['image'] and len(item['image']) > 1:
            for ind, image in enumerate(item['image']):
                print("Image " + str(ind+1) + ": " + image)
        elif item['image'] and item['image'][0]:
            print("Image:" + item['image'][0])
        if item['alt'] and len(item['alt']) > 1:
            for ind, alt in enumerate(item['alt']):
                print("Alt " + str(ind+1) + ": " + alt)
        elif item['alt'] and item['alt'][0]:
            print("Alt: " + item['alt'][0])
        print("Link: " + item['link'])
    print('------------------')


def json_convert(news):
    """Converts the news into JSON format"""
    log.info("Converting to JSON...")
    print(json.dumps(news, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))


def args_parse() -> argparse.Namespace:
    log.info("Parsing arguments...")
    parser = argparse.ArgumentParser(description="RSS")
    parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=999, help='Limit news topics if this parameter provided')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        log.info("Main")
        args = args_parse()
        if is_connected():
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
    except CustomEx as ex:
        print(ex.msg)
        print('Exiting the program')
        log.info('Exiting the program')
