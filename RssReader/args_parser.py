"""
This module process the input arguments
"""

import argparse
import re
import RssReader.logs as logs
import sys


def get_parse(args_in=''):
    """This function takes the arguments from command line"""

    parser = argparse.ArgumentParser(prog='RSSTaker', description='RSS reader. Takes the arguments from command line.')

    parser.add_argument('url', type=str, help='Link to RSS channel(line without spaces). Mandatory for all actions.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='Print version info.')
    parser.add_argument('-j', '--json', action='store_const', const=True, help='Print result as json in stdout.')
    parser.add_argument('-b', '--verbose', action='store_const', const=True, help='Print all logs in stdout.')
    parser.add_argument('-l', '--limit', type=int, default=1, help='Limit of news topics (natural number).')

    if args_in:
        try:
            args = parser.parse_args(args_in)
            logs.log_init_args(args)
        except SystemExit:
            logs.log_err_init_args(args_in)
            logs.log_err_exit()
            parser.exit()
    else:
        try:
            args = parser.parse_args()
            logs.log_init_args(args)
        except SystemExit:
            logs.log_err_init_args(sys.argv)
            logs.log_err_exit()
            parser.exit()

    return {'url': args.url, 'json': args.json, 'verbose': args.verbose, 'limit': args.limit}


def validate_url(url: str):
    """This function validates if RSS link is an actual URL"""

    url_check = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)

    if len(url_check) == 0:
        return False

    if len(url) != len(url_check[0]):
        return False
    else:
        return True


def validate_args(data: dict):
    """This function validates the arguments are correct"""

    if data['limit'] < 0:
        return False
    else:
        return True

