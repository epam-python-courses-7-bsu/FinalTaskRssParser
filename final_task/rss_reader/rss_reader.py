#!/usr/bin/env python3.8

from rss_reader import cmd_line_parser
from rss_reader import logger
from rss_reader import rss_parser


VERSION = 2.1


def main():
    # parse arguments received from the command line
    command_line_args = cmd_line_parser.PARSER.parse_args()
    cmd_line_parser.output_verbose(command_line_args, logger.LOGGER)

    news_parser = rss_parser.RSSparser(command_line_args, logger.LOGGER)
    if not command_line_args.json:
        news_parser.output_txt_news()
    cmd_line_parser.output_json(news_parser, command_line_args, logger.LOGGER)
    cmd_line_parser.output_version(command_line_args, VERSION, logger.LOGGER)


if __name__ == "__main__":
    main()
