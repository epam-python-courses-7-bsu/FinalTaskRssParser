#!/usr/bin/env python3.8

from cmd_line_parser import make_arg_parser, output_json, output_verbose, output_version
from logger import LOGGER
from rss_parser import RSSparser


VERSION = 2.1


def main():
    # parse arguments received from the command line
    parser = make_arg_parser()
    command_line_args = parser.parse_args()
    output_verbose(command_line_args, LOGGER)

    news_parser = RSSparser(command_line_args, LOGGER)
    if not command_line_args.json:
        news_parser.output_txt_news()
    output_json(news_parser, command_line_args, LOGGER)
    output_version(command_line_args, VERSION, LOGGER)


if __name__ == "__main__":
    main()
