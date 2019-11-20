#!/usr/bin/env python3.8

from cache import cache_news, get_cached_news
from cmd_line_parser import make_arg_parser, output_json, output_verbose, output_version
from logger import LOGGER
from rss_parser import RSSparser
from rss_printer import output_txt_news
from validator import check_the_connection, check_response_status_code


VERSION = 3.0


def main():
    # parse arguments received from the command line
    parser = make_arg_parser()
    command_line_args = parser.parse_args()
    output_verbose(command_line_args, LOGGER)

    if command_line_args.date:
        # retrieve data from the cache
        all_news = get_cached_news(command_line_args, LOGGER)
    else:
        # retrieve data from the internet
        check_the_connection(command_line_args, LOGGER)
        check_response_status_code(command_line_args, LOGGER)
        news_parser = RSSparser(command_line_args, LOGGER)
        all_news = news_parser.parse_feed()
        cache_news(all_news, LOGGER)

    if not command_line_args.json:
        output_txt_news(all_news, LOGGER)
    output_json(all_news, command_line_args, LOGGER)
    output_version(command_line_args, VERSION, LOGGER)


if __name__ == "__main__":
    main()
