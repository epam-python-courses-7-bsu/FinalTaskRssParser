"""
This module process the input arguments
"""

import argparse
import re
import logs
import sys
import datetime


def get_parse(args_in='') -> dict:
    """This function takes the arguments from command line"""

    parser = argparse.ArgumentParser(prog='RSSTaker', description='RSS reader. Takes the arguments from command line.')

    parser.add_argument('url', type=str, help='Link to RSS channel(line without spaces). Mandatory for all actions.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 3.1', help='Print version info.')
    parser.add_argument('-j', '--json', action='store_const', const=True, help='Print result as json in stdout.')
    parser.add_argument('-b', '--verbose', action='store_const', const=True, help='Print all logs in stdout.')
    parser.add_argument('-l', '--limit', type=int, default=1, help='Limit of news topics (natural number).')
    parser.add_argument('-d', '--date', type=int, help='Date to print news from history, yyyymmdd (natural number).')

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

    return {'url': args.url, 'json': args.json, 'verbose': args.verbose, 'limit': args.limit, 'date': args.date}


def validate_url(url: str) -> bool:
    """This function validates if RSS link is an actual URL"""

    url_check = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)

    if len(url_check) == 0:
        return False

    return len(url) == len(url_check[0])


def validate_args(data: dict) -> bool:
    """This function validates the arguments are correct"""

    date_time = datetime.datetime.now()

    if data['limit'] < 0:
        print('Limit is invalid.')
        return False

    if data['date']:
        if data['date'] > int(date_time.strftime("%Y%m%d")):
            print('Date is wrong: today date ' + date_time.strftime("%Y%m%d") + ' is less than your date.')
            return False
        else:
            return True

    return True


