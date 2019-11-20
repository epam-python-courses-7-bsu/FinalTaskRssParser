#!/usr/bin/env python3.8

import argparse
import datetime
import json
import logging

from rss_exceptions import InvalidDateFormat

def make_arg_parser():
    """
    Make a parser for parsing exact arguments out of sys.argv.
    :return: parser
    """
    parser = argparse.ArgumentParser(description="Performs a variety of operations on a file.")

    parser.add_argument('source', help='RSS URL', nargs='?', default='')
    parser.add_argument('--version', action="store_true", help="Print version info")
    parser.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
    parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
    parser.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=convert_date, help="Displays news for the specified day")
    return parser


def convert_date(date):
    """
    Converts an argument in  %%Y%%m%%d format to %d%m%Y format
    """
    try:
        date = datetime.datetime.strptime(date, '%Y%m%d')
        reformed_date = date.strftime("%d %b %Y")
        return reformed_date
    except ValueError:
        raise InvalidDateFormat('')


def output_json(all_news, cmd_args, logger):
    """
    While the 'json' argument was passed - converts data in json format and prints it
    """
    if cmd_args.json:
        logger.info('Output result of parsing RSS in JSON format')
        news_in_json = json.dumps(all_news, indent=4, ensure_ascii=False)
        print(news_in_json)


def output_verbose(cmd_args, logger):
    """
    While the 'verbose' argument was passed, func reports events
    that occur during normal operation of a program.
    """
    if cmd_args.verbose:
        logger.info('Output info logs in console.')
        logger.setLevel(logging.INFO)


def output_version(cmd_args, version, logger):
    """
    While the 'version' argument was passed - prints the program version
    """
    if cmd_args.version:
        logger.info('Output the RSS reader version')
        print(f"RSS_reader {version}")
