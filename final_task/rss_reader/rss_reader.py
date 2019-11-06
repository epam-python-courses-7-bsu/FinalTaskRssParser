import argparse
import html
import json
import feedparser
import logging
import urllib.request
import sys
import re
from typing import Tuple, List

import single_article
import custom_error

VERSION = 1.0
LOG_FILE_NAME = 'app.log'


def parse_rss(rss_url: str) -> feedparser.FeedParserDict:
    """Parse the rss"""
    return feedparser.parse(rss_url)


def get_source(parsed: feedparser.FeedParserDict) -> dict:
    """Returns dictionary with feed information."""
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }


def find_links_in_article(article: feedparser.FeedParserDict) -> list:
    """Finds links in the article"""
    image_search = re.compile(r'<\s*img [^>]*src="([^"]+)')
    img = image_search.findall(article['summary'])

    all_links = []
    for link in article['links']:
        if link['href'] not in img:
            all_links.append(link['href'])
    all_links += img

    return all_links


def unescape(text_to_unescape: str) -> str:
    """Unescape text"""
    return html.unescape(text_to_unescape)


def get_articles(parsed: feedparser.FeedParserDict, limit: int) -> Tuple[List[single_article.SingleArticle], int]:
    """Returns list with articles."""
    articles = []
    feed = parsed['feed']
    entries = parsed['entries']
    logging.info(f'There is {len(entries)} entries')

    no_tags = re.compile('<.*?>')

    if limit is None:
        limit = len(entries)

    try:
        for index, entry in enumerate(entries):
            if index == limit:
                break

            links_in_article = find_links_in_article(entry)

            if 'published' not in entry:
                limit -= 1
                continue
            articles.append(
                single_article.SingleArticle(
                    feed=unescape(feed['title']),
                    title=unescape(entry['title']),
                    date=entry['published'],
                    link=entry['link'],
                    summary=unescape(re.sub(no_tags, '', entry['summary'])),
                    links=[f"[{num}]: {link}" for num, link in enumerate(links_in_article, 1)])
            )
    except KeyError as value:
        raise custom_error.ArticleKeyError(f"One of the entries does not have {value} key")

    return articles, limit


def print_rss_json(data: List[single_article.SingleArticle]) -> None:
    """Prints result as JSON in stdout"""
    print(json.dumps(data, cls=single_article.EnhancedJSONEncoder, ensure_ascii=False))


def print_article(data: single_article.SingleArticle) -> None:
    """Prints a single article in stdout"""
    print("-" * 120)
    print(data)
    print("-" * 120)


def print_rss_articles(rss_articles: List[single_article.SingleArticle]) -> None:
    """Prints source feed and articles"""
    for article in rss_articles:
        print_article(article)


def check_if_verbose(args: argparse.Namespace) -> None:
    """Checks if verbose is on and prints logs to stdout"""
    if args.verbose:
        with open(LOG_FILE_NAME, 'r') as fin:
            print(fin.read(), end='')
        logging.info('Log was printed in stdout')


def main(args: argparse.Namespace) -> None:
    """The main entry point of the application"""
    rss_url = args.source
    limit = args.limit

    parsed_rss = parse_rss(rss_url)
    logging.info('RSS URL parsed')

    articles_list, limit = get_articles(parsed_rss, limit)
    logging.info('Articles list created')

    try:
        if args.json:
            print_rss_json(articles_list)
            logging.info('Articles was printed as json')
        else:
            print_rss_articles(articles_list)
            logging.info(f'{limit} articles was printed')
    except IndexError:
        logging.error('There is no articles by this URL')

    check_if_verbose(args)

    logging.info('Application ended')


def check_the_connection(rss_url: str) -> str:
    """Checks the connection"""
    info = ''
    try:
        urllib.request.urlopen(rss_url)
    except urllib.request.HTTPError as e:
        info = f'{e.code}: {e.reason}'
        return info
    except urllib.request.URLError as e:
        info = f'{e.reason}'
        return info
    else:
        return info


def check_if_link_is_correct(rss_url: str) -> bool:
    """Checks if link is valid"""
    try:
        result = urllib.request.urlparse(rss_url)
        return all([result.scheme, result.netloc, "." in result.netloc, len(result.netloc) > 2])
    except ValueError:
        return False


def check_url_and_connection(rss_url: str) -> None:
    """Checks if url is valid and connection successful"""
    if not check_if_help_or_version_in_arguments():
        if check_if_link_is_correct(rss_url):
            logging.info('Valid url')
            connection_info = check_the_connection(rss_url)
            if not connection_info:
                logging.info('Connection successful')
            else:
                raise custom_error.ConnectionFailedError(f"Connection failed: {connection_info}")
        else:
            raise custom_error.NotValidUrlError


def check_if_help_or_version_in_arguments() -> bool:
    """Checks if  '--help/-h' or '--version' in arguments"""
    flag = False
    if '--help' in sys.argv or '-h' in sys.argv:
        logging.info('Help was printed')
        logging.info('Application ended')
        flag = True
    elif '--version' in sys.argv:
        logging.info('Version was printed')
        logging.info('Application ended')
        flag = True
    return flag


def check_the_arguments_amount() -> None:
    """Checks if there only 1 argument and raises exception"""
    if len(sys.argv) == 1:
        raise custom_error.NotEnoughArgumentsError


def find_url() -> str:
    """Checks if url in args and puts it to sys.argv[1] else raises exception"""
    for index, value in enumerate(sys.argv):
        if "http" in value:
            if value.count("'") == 2:
                value = value[1:-1]
                sys.argv[index] = value
            if index != 1:
                sys.argv.insert(1, sys.argv.pop(index))
            return value

    raise custom_error.UrlNotFoundInArgsError


def create_parser() -> argparse.ArgumentParser:
    """Adding arguments to run the application"""
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("--version", action='version', version=f'%(prog)s version: {VERSION}',
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None, help="Limit news topics if this parameter provided")
    return parser


def start_logging() -> None:
    """Setting up logging basic configuration"""
    logging.basicConfig(
        filename=LOG_FILE_NAME,
        filemode='w',
        format=u'[%(asctime)s] %(levelname)-8s %(message)s',
        level=logging.DEBUG
    )


if __name__ == '__main__':
    try:
        start_logging()
        logging.info('Application started')

        arg_parser = create_parser()
        logging.info('Argument parser created')

        check_the_arguments_amount()

        url = find_url()

        check_url_and_connection(url)

        args_namespace = arg_parser.parse_args()
        main(args_namespace)

    except custom_error.UrlNotFoundInArgsError:
        logging.error('UrlNotFoundInArgsError')
        logging.info('Application ended')
        print("Url is not found in the arguments")
    except custom_error.NotEnoughArgumentsError:
        logging.error('Not enough arguments(URL link is required)')
        logging.info('Application ended')
        print("Not enough arguments(URL link is required)")
    except custom_error.NotValidUrlError:
        logging.error('Not valid url')
        logging.info('Application ended')
        print('Not valid url')
    except custom_error.ConnectionFailedError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print('Connection failed')
    except custom_error.ArticleKeyError as error:
        logging.error(error.message)
        logging.info('Application ended')

        # python rss_reader.py "https://news.yahoo.com/rss/"
        # python rss_reader.py "https://news.tut.by/rss/economics.rss"
        # python rss_reader.py 'http://rss.cnn.com/rss/edition_world.rss'
