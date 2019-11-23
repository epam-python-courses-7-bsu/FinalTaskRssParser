#!/usr/bin/env python3.8

import argparse
import datetime
import json
import logging
import sys

import coloredlogs
from termcolor import cprint

from rss_exceptions import FormatDateError


def make_arg_parser():
    """
    Make a parser for parsing exact arguments out of sys.argv
    :return: parser
    """
    parser = argparse.ArgumentParser(description="Performs a variety of operations on a file.")

    parser.add_argument('source', help='RSS URL', nargs='?', default='')
    parser.add_argument('--version', action='version', version=f'RSS-reader 5.0', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=None, help='Limits the number of displayed news')
    parser.add_argument('--date', type=convert_date, help='Displays news for the specified day')
    parser.add_argument('--to-html', type=str, default='',
                        help='Converts news in html format. Receives the path for file saving')
    parser.add_argument('--to-pdf', type=str, default='',
                        help='Converts news in pdf format. Receives the path for file saving.')
    parser.add_argument('--colorize', action='store_true', help='Make stdout in colour.')
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
        raise FormatDateError("Invalid date format. Date format should be like '%Y%m%d' -> 20191120.")


def output_json(all_news, cmd_args, logger):
    """
    If the 'json' argument was passed - converts data in json format and prints it
    """
    if cmd_args.json:
        logger.info('Convert RSS data in JSON format')
        news_in_json = json.dumps(all_news, indent=4, ensure_ascii=False)
        if cmd_args.colorize:
            logger.info('Output result of parsing RSS in colorized JSON format')
            cprint(news_in_json, 'cyan')
        else:
            logger.info('Output result of parsing RSS in JSON format')
            print(news_in_json)


def output_verbose(cmd_args):
    """
    If the 'verbose' argument was passed, func reports events
    that occur during normal operation of a program
    """
    if cmd_args.verbose:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(u'%(levelname)-8s [%(asctime)s] %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

        if cmd_args.colorize:
            coloredlogs.install()

