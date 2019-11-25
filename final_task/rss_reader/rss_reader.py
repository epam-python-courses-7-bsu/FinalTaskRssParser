import requests
import argparse
import json
import logging
import socket
import bs4
from bs4 import BeautifulSoup
import CustomException
from datetime import datetime
import converter
import colorizer
LOG = logging.getLogger("LOG")


def is_connected() -> bool:
    LOG.info("Checking internet connection...")
    try:
        socket.create_connection(("www.google.com", 80))
    except Exception:
        raise CustomException.ConnectionError
    return True


def find_news(url) -> bs4.element.ResultSet:
    """Parses news"""
    logging.info("Searching for news on " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll('item')
        LOG.info(f'{len(items)} pieces of news have been found')
    except requests.exceptions.MissingSchema:
        raise CustomException.WrongUrl
    except requests.exceptions.ConnectionError:
        LOG.error("Can't connect to the " + url)
        raise CustomException.UrlUnreachable
    return items


def find_channel(url) -> bs4.element.Tag:
    logging.info("Getting feed from " + url)
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        channel = soup.find('channel')
    except requests.exceptions.ConnectionError:
        raise CustomException.WrongUrl
    except requests.exceptions.InvalidURL:
        raise CustomException.WrongUrl
    except requests.exceptions.MissingSchema:
        raise CustomException.WrongUrl
    return channel


def collect_news(items, limit) -> list:
    """Sorts the components of the news into dictionaries and adds them into a list"""
    LOG.info("Collecting news...")
    news = []
    for item in items[slice(None, limit)]:
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
                    if not img['url'] in images:
                        images.append(img['url'])
            if item.content:
                for img in item.findAll('content'):
                    if not img['url'] in images:
                        images.append(img['url'])
            if item.enclosure:
                for img in item.findAll('enclosure'):
                    if not img['url'] in images:
                        images.append(img['url'])
            if not images:
                news_item['image'] = None
            else:
                news_item['image'] = images
            if soup.find('img'):
                for alt in soup.findAll('img'):
                    if not alt['alt'] in alts:
                        alts.append(alt['alt'])
            if item.find('media:text'):
                soup = BeautifulSoup(item.find('media:text').text, 'lxml')
                for alt in soup:
                    if not alt.find('img')['alt'] in alts:
                        alts.append(alt.find('img')['alt'])
            if not alts:
                news_item['alt'] = None
            else:
                news_item['alt'] = alts
        except TypeError:
            LOG.error("Could not load an image")
            news_item['image'] = "No image"
        except AttributeError:
            LOG.error("Probably no description")
            news_item['description'] = "No description"
        news.append(news_item)
    LOG.info(f'The limit of {limit} pieces of news reached')
    return news


def print_one(item, color):
    colorizer.print_blink('-------------------------------------------------------------', color)
    colorizer.print_main("Title: ", color)
    colorizer.printc(item['title'], color)
    colorizer.print_main("Date: ", color)
    colorizer.printc(item['date'], color)
    colorizer.print_main("Description: ", color)
    colorizer.printc(item['description'], color)
    if item['image'] and len(item['image']) > 1:
        for ind, image in enumerate(item['image']):
            colorizer.print_main(f'Image {ind + 1}: ' + image, color)
            print()
    elif item['image'] and item['image'][0]:
        colorizer.print_main("Image:", color)
        colorizer.print_link(item['image'][0], color)
    if not item['image']:
        colorizer.print_main("Alt: ", color)
        colorizer.printc(item['title'], color)
    elif item['alt'] and len(item['alt']) > 1 and len(item['image']) > 1:
        for ind, alt in enumerate(item['alt']):
            colorizer.print_main(f'Alt {ind + 1}:', color)
            colorizer.printc(alt, color)
            if ind + 1 == len(item['image']):
                break
    elif item['alt'] and item['alt'][0]:
        colorizer.print_main("Alt: ", color)
        colorizer.printc(item['alt'][0], color)
    colorizer.print_main("Link: ", color)
    colorizer.print_link(item['link'], color)


def print_news(list_of_news, channel, color):
    try:
        if channel:
            LOG.info('Searching for channel...')
            print("Feed: " + channel.title.text + '\n\n')
        for item in list_of_news:
            print_one(item, color)
    except AttributeError:
        raise CustomException.UrlUnreachable


def json_convert(news, color):
    """Converts the news into JSON format"""
    LOG.info("Converting to JSON...")
    colorizer.printc(json.dumps(news, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')), color)


def args_parse() -> argparse.Namespace:
    LOG.info("Parsing arguments...")
    parser = argparse.ArgumentParser(description="RSS")
    parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=999, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Specifies the date of news')
    parser.add_argument('--topdf', type=str, help='Converts news into PDF')
    parser.add_argument('--tohtml', type=str, help='Converts news into HTML')
    parser.add_argument('--colorize', action='store_true', help='Colorizes the output')
    return parser.parse_args()


def write_cache(news):
    LOG.info('Writing news to cache...')
    flag = True
    exists = True
    try:
        LOG.info('Trying to open cache file...')
        open('cache.json')
    except FileNotFoundError:
        LOG.info('Cache file does not exist yet')
        exists = False
    if exists:
        LOG.info('Creating a new cache file...')
        json_list = json.load(open('cache.json'))
        for item in news:
            for elem in json_list:
                if item['title'] == elem['title']:
                    flag = False
                    break
            if flag:
                json_list.append(item)
        with open("cache.json", "w") as file:
            json.dump(json_list, file, indent=2, ensure_ascii=False)
    else:
        with open("cache.json", "w") as file:
            json.dump(news, file, indent=2, ensure_ascii=False)


def get_by_date(datestr, source, limit, path_html, path_pdf, color, json_flag):
    if limit > 0:
        news = []
        date = datetime.strptime(datestr, '%Y%m%d').strftime("%d %b %Y")
        date = str(date)
        try:
            LOG.info('Opening cache...')
            with open('cache.json') as file:
                json_list = json.load(file)
        except FileNotFoundError:
            LOG.error('No news in cache')
            colorizer.printerr('No news in cache yet', color)
        else:
            LOG.info('Reading news from cache...')
            if source:
                source = source[8:source.find('/', 8)]
                for ind, item in enumerate(json_list):
                    if date in item['date'] and source in item['link']:
                        news.append(item)
                        if len(news) > limit - 1:
                            break
            else:
                for ind, item in enumerate(json_list):
                    if date in item['date']:
                        news.append(item)
                        if len(news) > limit - 1:
                            break

            if not news:
                LOG.error('No news on ' + date + ' have been found')
                colorizer.printerr('No news on ' + date + ' have been found', color)
            else:
                if not path_pdf and not path_html:
                    colorizer.print_blink('------------------- FROM CACHE ------------------------------\n\n', color)
                    colorizer.printc(date + ':\n', color)
                    if json_flag:
                        json_convert(news, color)
                    else:
                        print_news(news, None, color)
                if path_html:
                    converter.html_convert(news, limit, path_html, color)
                if path_pdf:
                    converter.pdf_convert(news, limit, path_pdf, color)


if __name__ == '__main__':
    flag = True
    try:
        LOG.info("Main")
        args = args_parse()
        if args.version:
            LOG.info(f'Version {args.version}')
            colorizer.printc('Version is 1.2', args.colorize)

        if args.verbose:
            logging.basicConfig(level=logging.INFO)
        if is_connected():

            if args.limit:
                limit = args.limit
                LOG.info(f'Limit = {limit}')
                if limit <= 0:
                    raise CustomException.WrongLimit

            if args.source:
                channel = find_channel(args.source)
                items = find_news(args.source)
                news = collect_news(items, limit)

                if args.json:
                    flag = False
                    json_convert(news, args.colorize)

                if args.tohtml and not args.date:
                    flag = False
                    converter.html_convert(news, limit, args.tohtml, args.colorize)

                if args.topdf and not args.date:
                    flag = False
                    converter.pdf_convert(news, limit, args.topdf, args.colorize)

                if flag and not args.date:
                    print_news(news, channel, args.colorize)
                write_cache(news)
    except CustomException.ConnectionError:
        colorizer.printerr('Can not connect to the internet. Check your connection', args.colorize)
    except CustomException.WrongLimit:
        LOG.error('Wrong limit')
        colorizer.printerr('Wrong limit', args.colorize)
    except CustomException.WrongUrl:
        colorizer.printerr('Wrong url ' + args.source, args.colorize)
    except CustomException.UrlUnreachable:
        colorizer.printerr('Can not make the connection with the site', args.colorize)
    if args.date:
        get_by_date(args.date, args.source, args.limit, args.tohtml, args.topdf, args.colorize, args.json)

