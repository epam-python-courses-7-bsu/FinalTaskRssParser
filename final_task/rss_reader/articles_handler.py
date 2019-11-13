import dataclasses
import datetime
import html
import json
import logging
import os
from typing import List, Tuple

import dateutil.parser
from bs4 import BeautifulSoup
import feedparser

import custom_error
import single_article

directory_to_module = os.path.abspath(os.path.dirname(__file__))
CACHE_FILE_NAME = directory_to_module + '\\cache.json'


def parse_rss(rss_url: str) -> feedparser.FeedParserDict:
    """Parse the rss"""
    return feedparser.parse(rss_url)


def create_rss_json(data: List[single_article.SingleArticle]):
    """Prints result as JSON in stdout"""
    return json.dumps(data, cls=single_article.EnhancedJSONEncoder, ensure_ascii=False)


def print_article(data: single_article.SingleArticle) -> None:
    """Prints a single article in stdout"""
    print("-" * 120)
    print(data)
    print("-" * 120)


def print_rss_articles(rss_articles: List[single_article.SingleArticle]) -> None:
    """Prints source feed and articles"""
    for article in rss_articles:
        print_article(article)


def find_links_in_article(article: feedparser.FeedParserDict) -> Tuple[List[str], str]:
    """Finds images and links in the article"""
    all_links = []

    soup = BeautifulSoup(article['summary'], features="html.parser")
    for index, img in enumerate(soup.find_all('img'), 1):
        if (str(img['src']) == '') and (str(img['alt']) == ''):
            continue
        if str(img['alt']) == '':
            all_links.append(str(img['src']))
            img.replaceWith(f"[image {index}: no description][{index}] ")
        elif str(img['src']) == '':
            img.replaceWith(f"[image(no link): {img['alt']}] ")
        else:
            all_links.append(str(img['src']))
            img.replaceWith(f"[image {index}: {img['alt']}][{index}] ")

    for link in article['links']:
        if link['href'] not in all_links:
            all_links.append(link['href'])

    return all_links, str(soup.text)


def unescape(text_to_unescape: str) -> str:
    """Unescape text"""
    return html.unescape(text_to_unescape)


def get_articles(parsed: feedparser.FeedParserDict, limit: int) -> List[single_article.SingleArticle]:
    """Returns list with articles."""
    articles = []
    feed = parsed['feed']
    entries = parsed['entries']
    logging.info(f'There is {len(entries)} entries')

    if limit is None:
        limit = len(entries)

    try:
        for index, entry in enumerate(entries):
            if index == limit:
                break

            date_info = 'unknown'
            if 'published' in entry:
                date_info = entry['published']

            links_in_article, summary_text = find_links_in_article(entry)
            articles.append(
                single_article.SingleArticle(
                    feed=unescape(feed['title']),
                    feed_url=feed['title_detail']['base'],
                    title=unescape(entry['title']),
                    date=date_info,
                    link=entry['link'],
                    summary=unescape(summary_text),
                    links=[f"[{num}]: {link}" for num, link in enumerate(links_in_article, 1)])
            )
    except KeyError as value:
        raise custom_error.ArticleKeyError(f"One of the entries does not have {value} key")

    return articles


def convert_dict_to_single_article(article_dict: dict) -> single_article.SingleArticle:
    """Converts dictionary to SingleArticle"""
    return single_article.SingleArticle(
        feed=unescape(article_dict['feed']),
        feed_url=article_dict['feed_url'],
        title=unescape(article_dict['title']),
        date=article_dict['date'],
        link=article_dict['link'],
        summary=unescape(article_dict['summary']),
        links=article_dict['links']
    )


class CachedArticlesClass:

    def __init__(self):
        self.cached_data_list = []

    def get_articles_from_cache(self) -> None:
        """Gets articles from cache file if it exists"""
        if not os.path.exists(CACHE_FILE_NAME) or os.stat(CACHE_FILE_NAME).st_size == 0:
            raise custom_error.NoDataInCacheFileError

        with open(CACHE_FILE_NAME, 'r') as cache_file:
            loaded_data_list = json.load(cache_file)
            parsed_data_list = json.loads(loaded_data_list)
            self.cached_data_list = parsed_data_list

    def save_articles_to_cache(self, articles_list: List[single_article.SingleArticle]) -> None:
        """
        Checks if cache file is exists
        if not creates it than writes read articles from internet to cache file
        else reads data from file and adds internet data to it than write data to cache
        """
        if not os.path.exists(CACHE_FILE_NAME):
            with open(CACHE_FILE_NAME, 'w'):
                pass

        with open(CACHE_FILE_NAME, 'r') as cache_file:
            if cache_file and os.stat(CACHE_FILE_NAME).st_size != 0:
                is_file_empty = False
                loaded_data_list = json.load(cache_file)
                parsed_data_list = json.loads(loaded_data_list)

                for value in articles_list:
                    converted_value = dataclasses.asdict(value)
                    if dataclasses.asdict(value) not in parsed_data_list:
                        parsed_data_list.append(converted_value)

                self.cached_data_list = parsed_data_list

                parsed_data_list_json = create_rss_json(parsed_data_list)
            else:
                is_file_empty = True

        with open(CACHE_FILE_NAME, 'w+') as cache_file:
            if not is_file_empty:
                json.dump(parsed_data_list_json, cache_file)
            else:
                json.dump(create_rss_json(articles_list), cache_file)

    def make_list_of_articles_by_date_and_url(self, date: datetime.datetime, url: str, limit: int) \
            -> List[single_article.SingleArticle]:
        """Find articles in cache by date and feed url"""

        list_of_articles_by_date = []
        counter = 0

        if not url:
            for cached_article in self.cached_data_list:
                if cached_article['date'] != 'unknown':
                    date_from_article = dateutil.parser.parse(cached_article['date'])

                    if (date.year == date_from_article.year) and \
                            (date.month == date_from_article.month) and \
                            (date.day == date_from_article.day):
                        list_of_articles_by_date.append(convert_dict_to_single_article(cached_article))
                        counter += 1
                        if counter == limit:
                            break
        else:
            for cached_article in self.cached_data_list:
                if cached_article['feed_url'] == url and cached_article['date'] != 'unknown':
                    date_from_article = dateutil.parser.parse(cached_article['date'])

                    if (date.year == date_from_article.year) and \
                            (date.month == date_from_article.month) and \
                            (date.day == date_from_article.day):
                        list_of_articles_by_date.append(convert_dict_to_single_article(cached_article))
                        counter += 1
                        if counter == limit:
                            break

        return list_of_articles_by_date
