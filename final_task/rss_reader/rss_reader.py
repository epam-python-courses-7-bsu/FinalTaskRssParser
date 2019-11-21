#! /usr/bin/env python
import argparse
import json
import logging
import sys
from urllib import request, error
from parser import xml_parser
from cache import update_cache, read_cache


def go_for_rss(url):
    """go for URL and get response"""
    try:
        logging.info(f'Started getting data from {url}')
        response = request.urlopen(url)
        logging.info(f'Data recieved from {url}')
    except error.HTTPError as ex:
        logging.info(ex)
        raise
    return response


def output_format(news_articles, json_output):
    """formating data to the format we choose. default='str'"""
    logging.info('Preparing output')
    if json_output:
        for article in news_articles:
            result = json.dumps(article.__dict__, ensure_ascii=False, indent=4)
            yield result
    else:
        for article in news_articles:
            yield article


def print_result(result, limit):
    """print output"""
    if limit:
        limit = int(limit)
        for article in result:
            if limit > 0:
                print(article)
                limit -= 1
    else:
        for article in result:
            print(article)


def get_args():
    """get arguments passed to script and parse it"""
    parser = argparse.ArgumentParser(description="Pure python command-line RSS reader")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="version", version='rss_reader 0.3.0')
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=int, help=("""Read cached news for provided URL.
                                                     If "ALL" provided - prints all cached news for this date"""))

    return parser.parse_args()


def main():
    """Entry point for RSS reader"""
    args = get_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    if not args.date:
        try:
            response = go_for_rss(args.source)
        except Exception as ex:
            print(ex)
            print('Website is not working or Url is not correct. Please, restart the program with a correct url')
            return None
        news_articles = xml_parser(response, args.limit)
        update_cache(news_articles, args.source)
    else:
        news_articles = read_cache(args.date, args.source)

    result = output_format(news_articles, args.json)
    print_result(result, args.limit)


if __name__ == "__main__":
    main()
