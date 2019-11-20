"""
This module interchange between Internet and program
"""

import feedparser
import html2text
import re
import datetime
import time
import urllib.request
import urllib.error
import http.client


server_answer = http.client.responses


def get_rss(url: str) -> dict:
    """This function receives the answer from server"""

    news = feedparser.parse(url)
    return news if news.entries else None


def process_rss(rss: dict, limit: int) -> dict:
    """This function process rss news"""

    data = dict()

    try:
        rss.entries[limit]
    except AttributeError:
        return False

    data['feed'] = rss.feed.title
    data['link'] = rss.entries[limit].link
    data['title'] = rss.entries[limit].title

    """news_date for third iteration, yyyy-mm-dd"""

    try:
        data['date'] = rss.entries[limit].published
        date_time = datetime.datetime.now()
        data['news_date'] = convert_date(rss.entries[limit].published)
    except AttributeError:
        date_time = datetime.datetime.now()
        data['date'] = date_time.strftime("%d/%m/%Y %H:%M:%S")
        data['news_date'] = date_time.strftime("%Y%m%d")

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
        try:
            img_try = rss.entries[limit].links[1]
            data['image'] = img_try['href']
        except IndexError:
            data['image'] = None
        except KeyError:
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


def connect_rss(url: str) -> bool:
    """This function tries to connect to RSS url
    In case of failure, it reconnects in 10 seconds
    """
    for connection_tryouts in range(3):

        try:
            tryout = urllib.request.urlopen(url).getcode()
            return tryout == 200

        # Everything deals with time delay will be repeated
        except urllib.error.HTTPError as http_err:
            if http_err.code in (503, 504, 522, 524):
                print('')
                print('The server is not available:')
                print('Trying to reconnect')

                """We wait between connection tryouts"""
                for time_delay in range(10):
                    print('. ', end='')
                    time.sleep(1)
                print('')

            # If server answer is a common code or something is not a common code
            elif http_err.code in server_answer.keys():
                print('The server can not be reached: Reason: %s' % server_answer[http_err.code])
                return False
            else:
                print('Unknown error: %s' % http_err.code)
                return False

        # In case HTTPError is not working
        except urllib.error.URLError as url_err:
            print('The server can not be reached. Reason: %s' % url_err.reason)

    return False


def convert_date(date: str):
    """This function converts date"""
    month = {'Jan': '1',
             'Feb': '2',
             'Mar': '3',
             'Apr': '4',
             'May': '5',
             'Jun': '6',
             'Jul': '7',
             'Aug': '8',
             'Sep': '9',
             'Oct': '10',
             'Nov': '11',
             'Dec': '12'}
    day = date[5:7]
    month_num = month[date[8:11]]
    year = date[12:16]

    return year+month_num+day
