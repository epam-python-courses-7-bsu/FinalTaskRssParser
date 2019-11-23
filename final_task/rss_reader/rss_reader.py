#!/usr/bin/env python3.8

from cache import cache_news, get_cached_news
from cmd_line_parser import make_arg_parser, output_json, output_verbose
from html_converter import convert_news_to_html
from logger import LOGGER
from pdf_converter import convert_news_to_pdf
import rss_exceptions as er
from rss_parser import RSSparser
from utils import output_txt_news
from validator import check_url_availability, check_response_status_code


def main():
    # parse arguments received from the command line
    parser = make_arg_parser()
    command_line_args = parser.parse_args()
    output_verbose(command_line_args)

    if command_line_args.date:
        # retrieve data from the cache
        all_news = get_cached_news(command_line_args, LOGGER)
    else:
        # retrieve data from the internet
        check_url_availability(command_line_args, LOGGER)
        check_response_status_code(command_line_args, LOGGER)
        news_parser = RSSparser(command_line_args, LOGGER)
        all_news = news_parser.parse_feed()
        cache_news(all_news, LOGGER)

    convert_news_to_html(command_line_args, all_news, LOGGER)
    convert_news_to_pdf(command_line_args, all_news, LOGGER)

    if not command_line_args.json:
        output_txt_news(command_line_args, all_news, LOGGER)

    output_json(all_news, command_line_args, LOGGER)


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
            er.URLResponseError
    ) as error:
        LOGGER.error(str(error))
        print(error)

    except er.InternetConnectionError as error:
        LOGGER.error("ConnectionError: " + str(error))
        print("ConnectionError: ", error)

    except er.UnreachableURLError as error:
        LOGGER.error('Unreachable Url: ' + str(error))
        print('Unreachable Url: ', error)
