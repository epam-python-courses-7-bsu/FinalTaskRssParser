"""
This module interchange between Internet and program
"""

import RssReader.feedparser as feedparser
import RssReader.html2text as html2text
import re
import datetime
import time
import urllib.request


def get_rss(url: str):
    """This function receives the answer from server"""

    news = feedparser.parse(url)
    if news.entries:
        return news
    else:
        return None


def process_rss(rss: dict, limit: int):
    """This function process rss news"""

    data = dict()

    try:
        rss.entries[limit]
    except AttributeError:
        return False

    data['feed'] = rss.feed.title
    data['link'] = rss.entries[limit].link
    data['title'] = rss.entries[limit].title

    try:
        data['date'] = rss.entries[limit].published
    except AttributeError:
        date_time = datetime.datetime.now()
        data['date'] = date_time.strftime("%d/%m/%Y %H:%M:%S")

    try:
        data['description'] = rss.entries[limit].summary_detail['value']
        data['image'] = rss.entries[limit].summary_detail['value']
    except AttributeError:
        data['description'] = rss.entries[limit].title_detail['value']
        data['image'] = rss.entries[limit].title_detail['value']

    data['description'] = re.sub('<p><a.+></a>', '',  data['description'])
    data['description'] = re.sub('<br.+clear="all">', '', data['description'])
    data['description'] = re.sub('<img.+/>', '',  data['description'])
    data['description'] = html2text.html2text(data['description'])

    img_raw = re.search('><img src=".+"', data['image'])

    if img_raw is not None:
        img_clean = img_raw[0].replace('><img src="', '')
        img_clean = re.sub('".+"', '', img_clean)
        data['image'] = img_clean
    else:
        data['image'] = None

    return data


def print_rss(data: dict):
    """This function prints data in a readable form"""

    print('Feed: ' + data['feed'])
    print('Title: ' + data['title'])
    print('Date: ' + data['date'])
    print('Link: ' + data['link'] + '\n')
    print(data['description'], end='')

    if data['image'] is not None:
        print('Image: ' + data['image'])
        print('. . . . . . . . . . . . . . . . . . . . . .')
        print('')
    else:
        print('Image: image is not available.')
        print('. . . . . . . . . . . . . . . . . . . . . .')
        print('')


def connect_rss(url: str):
    """This function tries to connect to RSS url
    In case of failure, it reconnects in 10 seconds
    """

    for i in range(3):
        try:
            a = urllib.request.urlopen(url).getcode()
        except urllib.error.URLError:
            a = 'Error'
        if a == 200:
            return True
        else:
            print('')
            print('The server is not available')
            print('Trying to reconnect')
            for j in range(10):
                print('. ', end='')
                time.sleep(1)
            print('')

    return False

