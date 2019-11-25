#!/usr/bin/env python3.8
"""The rss_reader.py file launches the entire application"""

import os
import sys

from cache import cache_news, get_cached_news
from cmd_line_parser import make_arg_parser, output_json, output_verbose
from html_converter import convert_news_to_html
from logger import LOGGER
from pdf_converter import convert_news_to_pdf
import rss_exceptions as er
from rss_parser import RSSparser
from utils import output_txt_news
import validator as valid


current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
os.chdir(current_dir)


def main():
    # parse arguments received from the command line
    parser = make_arg_parser()
    command_line_args = parser.parse_args()
    output_verbose(command_line_args)

    if command_line_args.date:
        # retrieve data from the cache
        valid.check_limit_value(command_line_args.limit)
        all_news = get_cached_news(command_line_args)
    else:
        # retrieve data from the internet
        valid.check_internet_connection()
        valid.check_url_availability(command_line_args)
        valid.check_response_status_code(command_line_args)
        news_parser = RSSparser(command_line_args)
        all_news = news_parser.parse_feed()
        cache_news(all_news)

    convert_news_to_html(command_line_args, all_news)
    convert_news_to_pdf(command_line_args, all_news)

    if not command_line_args.json:
        output_txt_news(command_line_args, all_news)

    output_json(all_news, command_line_args)


if __name__ == "__main__":
    try:
        main()
    except (
            er.EmptyCacheError,
            er.FeedError,
            er.FormatDateError,
            er.LimitSignError,
            er.PATHError,
            er.SpecifiedDayNewsError,
            er.UnreachableURLError,
            er.UndefinedURL,
            er.URLResponseError
    ) as error:
        LOGGER.error(str(error))
        print('Error: ', error)

    except er.InternetConnectionError as error:
        LOGGER.error("ConnectionError: " + str(error))
        print("ConnectionError: ", error)
