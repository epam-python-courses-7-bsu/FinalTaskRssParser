import json
import re
import signal
import logging
from contextlib import contextmanager
from urllib.error import URLError
import feedparser
from dateutil import parser
import News
import html
from exceptions import *

module_logger = logging.getLogger("rss_reader.scripts.parser_rss")


@contextmanager
def timeout_sec(seconds):
    """
       contextmanager to check the expectation of a response
       and if the response does not come for a long time, an error
    """

    def signal_handler(signum, frame):
        raise TimeOutExeption(Exception('Time out'))

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def clear_text(text: str) -> str:
    """
     cleans text from problems that occurred when decoding formats
    """
    logger = logging.getLogger("rss_reader.scripts.parser_rss.clear_text")
    logger.info("clear text from news")
    return html.unescape(text)


def get_info_about_image(summary: str) -> str:
    logger = logging.getLogger("rss_reader.scripts.parser_rss.get_info_about_image")
    logger.info("return info about image")
    tag = 'alt='
    begin_position_info_about_image = summary.find(tag) + len(tag) + 1
    end_position_info_about_image = summary.find('"', begin_position_info_about_image)
    info_about_image = summary[begin_position_info_about_image:end_position_info_about_image]
    return clear_text(info_about_image)


def get_briefly_about_news(summary: str) -> str:
    logger = logging.getLogger("rss_reader.scripts.parser_rss.get_briefly_about_news")
    logger.info("return briefly info about news")
    p = re.compile(r'<.*?>')
    text = p.sub('', summary)
    return clear_text(text)


def get_news_feed(sourse_url: str) -> feedparser.parse:
    logger = logging.getLogger("rss_reader.scripts.parser_rss.get_news_feed")
    logger.info("return news Feed")
    with timeout_sec(10):
        news_feed = feedparser.parse(sourse_url)
    if news_feed['bozo'] != 0:
        raise URLError(news_feed['bozo_exception'].args[0])
    return news_feed


def init_list_of_news(
        list_of_news: list,
        news_feed: feedparser.parse,
        limit: int):
    """
    Fills the list with news
    """
    logger = logging.getLogger("rss_reader.scripts.parser_rss.init_list_of_news")
    logger.info("Fills the list with news")
    feed_title = news_feed['feed'].get('title', 'NO TITLE')
    feed_title = clear_text(feed_title)
    for index, entry in enumerate(news_feed['entries']):
        if index == limit:
            break
        title = entry.get('title', '(NO TITLE')
        title = clear_text(title)
        summary = entry.get('summary', '(NO SUMMARY)')
        date = parser.parse(entry['published'])
        link = entry['link']
        info_about_image = get_info_about_image(summary)
        briefly_about_news = get_briefly_about_news(summary)
        link_on_image = entry.get("media_content")[0]["url"]
        news = News.News(feed=feed_title,
                         title=title,
                         date=date,
                         link=link,
                         info_about_image=info_about_image,
                         briefly_about_news=briefly_about_news,
                         links_from_news=[link, link_on_image]
                         )

        list_of_news.append(news)


def print_news(list_of_news: list):
    """
    This function print news in the console
    :param feed_title:
    :param list_of_news:
    :return:
    """
    logger = logging.getLogger("rss_reader.scripts.parser_rss.print_news")
    logger.info("print news in the console")
    for number, news in enumerate(list_of_news):
        print(number + 1)  # because number starts at 0
        print(news)
        # print('-' * 100)


def print_news_in_json(list_of_news: list):
    """
    This function print news in the console in json format
    :param list_of_news:
    :return:
    """
    logger = logging.getLogger("rss_reader.scripts.parser_rss.print_news_in_json")
    logger.info("print news in the console in json format")
    list_of_news_in_json = []
    for news in list_of_news:
        list_of_news_in_json.append(news.get_json())
    print(json.dumps(list_of_news_in_json, indent=4, ensure_ascii=False))
