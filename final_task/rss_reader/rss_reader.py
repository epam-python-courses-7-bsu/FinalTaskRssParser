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
                    alts.append(alt['alt'])
            if item.find('media:text'):
                soup = BeautifulSoup(item.find('media:text').text, 'lxml')
                for alt in soup:
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
        if len(news) == limit:
            LOG.info(f'The limit of {limit} pieces of news reached')
            break
    return news


def print_one(item):
    print("Title: " + item['title'])
    print("Date: " + item['date'])
    print("Description: " + item['description'])
    if item['image'] and len(item['image']) > 1:
        for ind, image in enumerate(item['image']):
            print(f'Image {ind + 1}: ' + image)
    elif item['image'] and item['image'][0]:
        print("Image:" + item['image'][0])
    if not item['image']:
        print("Alt: " + item['title'])
    elif item['alt'] and len(item['alt']) > 1 and len(item['image']) > 1:
        for ind, alt in enumerate(item['alt']):
            print(f'Alt {ind + 1}:' + alt)
            if ind + 1 == len(item['image']):
                break
    elif item['alt'] and item['alt'][0]:
        print("Alt: " + item['alt'][0])
    print("Link: " + item['link'])
    print('------------------')


def print_news(list_of_news, channel):
    try:
        if channel:
            print("Feed: " + channel.title.text + '\n\n')
        for item in list_of_news:
            print_one(item)
    except AttributeError:
        raise CustomException.UrlUnreachable


def json_convert(news):
    """Converts the news into JSON format"""
    LOG.info("Converting to JSON...")
    print(json.dumps(news, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))


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
    return parser.parse_args()


def write_cache(news):
    LOG.info('Writing news to cache...')
    flag = True
    exists = True
    try:
        open('cache.json')
    except FileNotFoundError:
        exists = False
    if exists:
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


def get_by_date(datestr, source, limit, html_flag, pdf_flag, path_html, path_pdf):
    if limit > 0:
        news = []
        flag = False
        date = datetime.strptime(datestr, '%Y%m%d').strftime("%d %b %Y")
        date = str(date)
        try:
            with open('cache.json') as file:
                json_list = json.load(file)
        except FileNotFoundError:
            print('No news in cache yet')
        else:
            if source:
                source = source[8:source.find('/', 8)]
                for ind, item in enumerate(json_list):
                    if date in item['date'] and source in item['link']:
                        flag = True
                        news.append(item)
                        if len(news) > limit - 1:
                            break
            else:
                for ind, item in enumerate(json_list):
                    if date in item['date']:
                        flag = True
                        news.append(item)
                        if len(news) > limit - 1:
                            break

            if not flag:
                LOG.error('No news on ' + date + ' have been found')
                print('No news on ' + date + ' have been found')
            else:
                if not html_flag and not pdf_flag:
                    print('------------------- FROM CACHE ------------------------------\n\n')
                    print(date + ':\n')
                    print_news(news, None)
                if html_flag:
                    converter.html_convert(news, limit, path_html)
                if pdf_flag:
                    converter.pdf_convert(news, limit, path_pdf)


if __name__ == '__main__':
    flag = True
    html_flag = False
    pdf_flag = False
    try:
        LOG.info("Main")
        args = args_parse()
        if args.version:
            LOG.info(f'Version {args.version}')
            print('Version is 1.2')

        if args.verbose:
            logging.basicConfig(level=logging.INFO)
        if is_connected():

            if args.limit:
                limit = args.limit
                LOG.info(f'Limit = {limit}')
                if limit <= 0:
                    raise CustomException.WrongLimit

            if args.source:
                if 'www' in args.source:
                    args.source = args.source[:8] + args.source[12:]
                channel = find_channel(args.source)
                items = find_news(args.source)
                news = collect_news(items, limit)

                if args.json and not args.topfd and not args.tohtml:
                    flag = False
                    json_convert(news)

                if args.tohtml:
                    flag = False
                    converter.html_convert(news, limit, args.tohtml)

                if args.topdf:
                    flag = False
                    converter.pdf_convert(news, limit, args.topdf)

                if flag:
                    print_news(news, channel)

                write_cache(news)

                if args.date:
                    print('\n\n\n\n')

    except CustomException.ConnectionError:
        print('Can not connect to the internet. Check your connection')
    except CustomException.WrongLimit:
        LOG.error('Wrong limit')
        print('Wrong limit')
    except CustomException.WrongUrl:
        print('Wrong url ' + args.source)
    except CustomException.UrlUnreachable:
        print('Can not make the connection with the site')
    if args.date:
        if args.tohtml:
            html_flag = True
        if args.topdf:
            pdf_flag = True
        get_by_date(args.date, args.source, args.limit, html_flag, pdf_flag, args.tohtml, args.topdf)
