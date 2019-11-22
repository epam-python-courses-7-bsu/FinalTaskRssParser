import argparse
import os
import re
import logging
from custom_exceptions import IncorrectFilePath


def get_arguments():
    """
    :return: Arguments of application
    Read and returns arguments of application
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    argument_parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
    argument_parser.add_argument('--version', action='store_true', help='print version info')
    argument_parser.add_argument('--limit', help='limit news topics if this parameter provided')
    argument_parser.add_argument('--date', help='represent news from local storage by date')
    argument_parser.add_argument('--to-html', help='save news in html format')
    argument_parser.add_argument('--to-fb2', help='save news in fb2 format')
    argument_parser.add_argument('--colorize', action='store_true', help='print news in colorized mode')
    argument_parser.add_argument('source', nargs='?')
    return argument_parser.parse_args()


def check_html_argument(html_argument):
    """
    :param html_argument: html directory path
    If argument wrong raises exception
    """
    if not os.path.exists(html_argument):
        logging.error('Inrorrect html filepath')
        raise IncorrectFilePath('Inrorrect html filepath')


def check_fb2_argument(fb2_argument):
    """
       :param fb2_argument: fb2 directory path
       If argument wrong raises exception
       """
    if not os.path.exists(fb2_argument):
        logging.error('Inrorrect fb2 filepath')
        raise IncorrectFilePath('Inrorrect fb2 filepath')


def check_limit_argument(limit_argument):
    """
          :param limit_argument: limit of news
          If argument wrong raises exception
          """
    if not re.match('\\d+', limit_argument):
        logging.error('Input value of --limit is incorrect')
        raise ValueError('Input value of --limit is incorrect')


def check_date_argument(date_argument):
    """
              :param date_argument: Date of news in database
              If argument wrong raises exception
              """
    if not re.match('\\d+', date_argument) or len(date_argument) != 8:
        logging.error('Input value of --date is incorrect')
        raise ValueError('Input value of --date is incorrect')
