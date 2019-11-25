import logging
import argparse

from bs4 import BeautifulSoup

from news_articles import NewsArticle


def xml_parser(response, limit):
    """get response and parse it to get NewsArticle object"""
    logging.info('Starting to parse XML data')
    soup = BeautifulSoup(response, 'xml')
    news_outlett_name = soup.title.text
    # get items from xml. each item it is an article
    news_soup = soup('item')
    news_articles = []
    for article in news_soup:
        if limit and len(news_articles) >= limit:
            break
        pub_date = article.pubDate.text
        news_link = article.link.text

        # make the soup again because codes such as &#39; were not decoded at first step
        news_title = BeautifulSoup(article.title.text, 'lxml').text
        if article.find('description'):
            # make soup again because we couldn't go deeper down the tree(couldn't recognize some tags)
            # in case of complex nesting in xml code
            description_soup = BeautifulSoup(article.description.text, 'lxml')
            news_description = description_soup.text
            if description_soup.find('img'):
                img_alt = description_soup.img.get('alt')
                img_src = description_soup.img.get('src')
            else:
                img_alt = ''
                img_src = ''
            news_articles.append(NewsArticle(news_outlett_name, news_title, pub_date, news_link,
                                             news_description, img_alt, img_src))
        else:
            news_description = ''
            news_articles.append(NewsArticle(news_outlett_name, news_title, pub_date, news_link,
                                             news_description))
    logging.info('Parsing is finished')
    return news_articles


def get_args():
    """get arguments passed to script and parse it"""
    parser = argparse.ArgumentParser(description="Pure python command-line RSS reader")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="version", version='rss_reader 0.4.0')
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=check_positive, help="Limit news topics if this parameter provided")
    parser.add_argument("--date",
                        type=check_digit,
                        help=("""Read cached news for provided URL.
                                 If "ALL" provided in source instead of URL - prints all cached news for this date"""))
    parser.add_argument("--to_html", type=str, help="Convert news to html and save it in path")
    parser.add_argument("--to_pdf", type=str, help="Convert news to pdf and save it in path")

    return parser.parse_args()


def check_positive(value):
    check_digit(value)
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError(f"can only be positive. Your input = {value}.")
    return value


def check_digit(value):
    if not value.isdigit():
        raise argparse.ArgumentTypeError(f"can only be integer. Your input = {value}.")
    return value
