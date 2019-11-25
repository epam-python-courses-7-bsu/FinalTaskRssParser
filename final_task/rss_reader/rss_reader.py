#! /usr/bin/env python
import json
import logging
import sys
import os
from urllib import request

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # noqa #402

from exceptions import CacheNotFoundError, GoForRssError, WrongResponseTypeError, NoDataToConvertError
from rss_parser import xml_parser, get_args
from cache import save_cache, read_cache
from converter import converter


def go_for_rss(url):
    """go for URL and get response"""
    try:
        logging.info(f'Started getting data from {url}')
        response = request.urlopen(url)
        logging.info(f'Data recieved from {url}')
        return response
    except Exception:
        raise GoForRssError


def check_response(response):
    """check content-type if it is a rss feed or not"""
    content_types = ["application/xml", "application/rss+xml", "text/xml"]
    for type_ in content_types:
        if response.headers['Content-Type'].startswith(type_):
            return response
    raise WrongResponseTypeError


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


def main():
    """Entry point for RSS reader"""
    try:
        args = get_args()
        if args.verbose:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

        if not args.date:
            response = check_response(go_for_rss(args.source))
            news_articles = xml_parser(response, args.limit)
            save_cache(news_articles, args.source)
        else:
            news_articles = read_cache(args.date, args.source, args.limit)

        if args.to_html or args.to_pdf:
            converter(news_articles, args.to_html, args.to_pdf)
        else:
            result = output_format(news_articles, args.json)
            print_result(result, args.limit)
    except CacheNotFoundError as ex:
        print(ex.__doc__)
    except GoForRssError as ex:
        print(ex.__doc__)
    except WrongResponseTypeError as ex:
        print(ex.__doc__)
    except NoDataToConvertError as ex:
        print(ex.__doc__)


if __name__ == "__main__":
    main()
