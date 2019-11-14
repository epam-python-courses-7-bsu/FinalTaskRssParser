#!/usr/bin/env python3.8

import argparse
import json
import logging


# Make a parser for parsing exact arguments out of sys.argv.
PARSER = argparse.ArgumentParser(description="Performs a variety of operations on a file.")

PARSER.add_argument('source', help='RSS URL')
PARSER.add_argument('--version', action="store_true", help="Print version info")
PARSER.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
PARSER.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
PARSER.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")


def output_json(news_parser, arguments, logger):
    """
    While the 'json' argument was passed - converts data in json format and prints it
    """
    if arguments.json:
        logger.info('Output result of parsing RSS in JSON format')
        news_in_json = json.dumps(news_parser.all_news)
        print(news_in_json)


def output_verbose(arguments, logger):
    """
    While the 'verbose' argument was passed, func reports events that occur during normal operation of a program
    """
    if arguments.verbose:
        logger.info('Output info logs in console.')
        logger.setLevel(logging.INFO)


def output_version(arguments, version, logger):
    """
    While the 'version' argument was passed - prints the program version
    """
    if arguments.version:
        logger.info('Output the RSS reader version')
        print(f"RSS_reader {version}")
