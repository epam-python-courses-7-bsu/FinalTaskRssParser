import feedparser
import argparse
import html2text
from requests import get
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, help='Please enter a valid URL for RSS Feed')
parser.add_argument('--limit', type=int, default=1, help='You can set a limit for news')
parser.add_argument('--verbose', type=bool, default=False, help='If you want to know '
                                                                'what\'s happening, set this to True')
parser.add_argument('--version', type=str, default=False, help='Print version of program')
args = parser.parse_args()
url = args.url
verbose = args.verbose
version = '[Reader version: 0.01]'


def to_text(html, rehtml=False):
    """
    This function creates instance of html2text.HTML2text
    and configuring it.
    We will use this to cleanup all HTML markup in our feed
    :param html: Text to format
    :param rehtml: True or False
    :return: formatted text
    """
    formatter = html2text.HTML2Text()
    formatter.wrap_links = False
    formatter.skip_internal_links = True
    formatter.inline_links = True
    formatter.ignore_anchors = True
    formatter.ignore_images = True
    formatter.ignore_emphasis = True
    formatter.ignore_links = True
    text = formatter.handle(html)
    text = text.strip(' \t\n\r')
    if rehtml:
        text = text.replace('\n', '<br/>')
        text = text.replace('\\', '')
    return text


def check_url(url: str, verbose: bool):
    """
    This function checks url provided by user
    Function will check if Content-Type of document on url
    is xml
    :param url: url provided by user
    :param verbose: True or False
    :return: True in case of xml,
    False and closing program in all other cases
    """
    if verbose:
        print('Wait a second, we will check if there is any RSS in URL you have given')
        print('-' * 50)
    response = get(url)
    r = response.headers['Content-Type']  # We will check only headers
    if 'xml' not in r:
        print('Something went wrong. \n'
              'Looks like URL you\'ve entered doesn\'t content any RSS feed')
        return False
    else:
        return True


def get_feed(url: str, verbose: bool):
    """
    Caching feed by creating a feedparser instance.
    Returns non-formatted feed
    :param url: url provided by user
    :param verbose: True of False
    :return: non-formatted feed
    """
    if verbose:
        print('Establishing connection')
        print('-' * 50)
    feed = feedparser.parse(url)
    if feed is None:
        print('STOP')
    if verbose:
        print('Connection established')
        print('-' * 50)
    return feed


def format_feed(feed, verbose: bool, limit: int):
    """
    This function recieves feed and format all entries
    by using them as to_text() arguments to remove
    all HTML markup
    :param feed: Cached feed returned by get_feed()
    :param verbose: True or False
    :param limit: Standart limit is 1 article
    :return: title, entry_title(Article title), description(Text of article), date
    """
    global title, entry_title, description, date
    if verbose:
        print('Formatting your feed')
        print('-' * 50)
    try:
        title = to_text(feed.feed.title)
        entry_title = to_text(feed.entries[limit].title)
        description = to_text(feed.entries[limit].description)
        date = to_text(feed.entries[limit].published)
    except AttributeError as error: # in case of AttributeError exception
        with open('log' + str(datetime.now()) + '.txt', 'w') as log:  # we will create a .txt log-file
            log.write('[URL]: ' + str(url) + '\n')  # providing info about feed that raised an exception
            log.write('[ERROR]: ' + str(error) + '\n')  # and text of error
        print('An error has occured \n'
              'Log file was created in program folder \n'
              'To help us debug a program, please send this file to h4j0rx@gmail.com')
    return title, entry_title, description, date


def main(title, entry_title, description, date):
    """
    This function just prints all parameters given by format_feed()
    :param title: Title of whole feed returned by format_feed()
    :param entry_title: Title of one article returned by format_feed()
    :param description: Description of one article returned by format_feed()
    :param date: Publishing date of one article returned by format_feed()
    :return: None
    """
    print('[URL]: ' + args.url)
    print('[Feed]: ' + title)
    print('-' * 50)
    print('[Title]: ' + entry_title)
    print('[Text]: ' + description)
    print('[Date]: ' + date)
    return None


if __name__ == '__main__':
    if args.url is None:
        print('Please enter a valid URL for a feed '
              'and run program like "python3 main.py '
              '--url %YOUR FEED URL%')
    if args.limit == 0:
        print('You have entered zero values to print, please specify another limit value')
    else:
        feed = get_feed(url, verbose)
        limit = [i for i in range(0, args.limit+1)]
        del limit[-1]
        for i in limit:
            format_feed(feed, verbose, i)
            main(title, entry_title, description, date)
        if args.version:
            print(version)