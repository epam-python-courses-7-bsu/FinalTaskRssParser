import argparse
import feedparser
import logging
import urllib.request
import json
import dataclasses
from dataclasses import dataclass
import sys
import re

VERSION = 1.0
LOG_FILE_NAME = 'app.log'


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, data_class):
        if dataclasses.is_dataclass(data_class):
            return dataclasses.asdict(data_class)
        return super().default(data_class)


@dataclass
class SingleArticle:
    feed: str
    title: str
    date: str
    link: str
    summary: str
    links: list

    def __str__(self) -> str:
        """Makes str with data of instance of a class"""
        str_for_print = f"Feed: {self.feed}\n" \
                        f"Title: {self.title}\n" \
                        f"Date: {self.date}\n" \
                        f"Link: {self.link}\n" \
                        f"{self.summary}\n"
        for link in self.links:
            str_for_print += f"{link}\n"
        return str_for_print


def parse_rss(url: str) -> feedparser.FeedParserDict:
    """Parse the rss"""
    return feedparser.parse(url)


def get_source(parsed: feedparser.FeedParserDict) -> dict:
    """Returns dictionary with feed information."""
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }


def get_articles(parsed: feedparser.FeedParserDict, limit: int) -> list:
    """Returns list with articles."""
    articles = []
    feed = parsed['feed']
    entries = parsed['entries']
    no_tags = re.compile('<.*?>')

    try:
        for index, entry in enumerate(entries):
            if index == limit:
                break
            articles.append(
                SingleArticle(
                    feed=feed['title'],
                    title=entry['title'],
                    date=entry['published'],
                    link=entry['link'],
                    summary=re.sub(no_tags, '', entry['summary']),
                    links=[f"[{num}]: {link['href']}" for num, link in enumerate(entry['links'], 1)])
            )
    except KeyError as value:
        logging.error(f"One of the entries does not have {value} key")
        logging.info('Application ended')
        sys.exit()

    return articles


def print_rss_json(data: list) -> None:
    """Prints result as JSON in stdout"""
    print(json.dumps(data, cls=EnhancedJSONEncoder))


def print_article(data: SingleArticle) -> None:
    """Prints a single article in stdout"""
    print("-" * 120)
    print(data)
    print("-" * 120)


def print_rss_articles(rss_articles: list) -> None:
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

    articles_list = get_articles(parsed_rss, limit)
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


def check_the_connection() -> str:
    """Checks the connection"""
    info = ''
    try:
        urllib.request.urlopen(sys.argv[1])
    except urllib.request.HTTPError as e:
        info = f'{e.code}: {e.reason}'
        return info
    except urllib.request.URLError as e:
        info = f'{e.reason}'
        return info
    else:
        return info


def check_if_link_is_correct() -> bool:
    """Checks if link is valid"""
    try:
        result = urllib.request.urlparse(sys.argv[1])
        return all([result.scheme, result.netloc, "." in result.netloc, len(result.netloc) > 2])
    except ValueError:
        return False


def check_url_and_connection() -> None:
    """Checks if url is valid and connection successful"""
    if not check_if_help_or_version_in_arguments():
        if check_if_link_is_correct():
            logging.info('Valid url')
            connection_info = check_the_connection()
            if connection_info:
                print('Connection failed')
                logging.error(f"Connection failed: {connection_info}")
                logging.info('Application ended')
                sys.exit()
            else:
                logging.info('Connection successful')
        else:
            logging.error('Not valid url')
            logging.info('Application ended')
            print('Not valid url')
            sys.exit()


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
    if len(sys.argv) == 1:
        logging.error('Not enough arguments(URL link is required)')
        logging.info('Application ended')
        print("Not enough arguments(URL link is required)")
        arg_parser.print_usage()
        sys.exit()


def create_parser() -> argparse.ArgumentParser:
    """Adding arguments to run the application"""
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("--version", action='version', version=f'%(prog)s version: {VERSION}',
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=1, help="Limit news topics if this parameter provided")
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
    start_logging()
    logging.info('Application started')

    arg_parser = create_parser()
    logging.info('Argument parser created')

    check_the_arguments_amount()

    check_url_and_connection()

    args_namespace = arg_parser.parse_args()
    main(args_namespace)
