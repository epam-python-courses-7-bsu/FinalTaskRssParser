import argparse
import datetime
import logging
import os
import sys
import urllib.request
from typing import Optional

import custom_error

VERSION = 4.0


def check_if_date_in_arguments() -> bool:
    """Checks if date is arguments"""
    if '--date' in sys.argv:
        return True
    else:
        return False


def check_if_help_or_version_in_arguments() -> Optional[str]:
    """Checks if help or version in arguments"""
    if '--help' in sys.argv or '-h' in sys.argv:
        return 'help'
    elif '--version' in sys.argv:
        return 'version'
    else:
        return None


def check_the_arguments_amount() -> None:
    """Checks if there only 1 argument and raises exception"""
    if len(sys.argv) == 1:
        raise custom_error.NotEnoughArgumentsError


def link_found() -> bool:
    """Checks if link in arguments"""
    for index, value in enumerate(sys.argv):
        if "http" in value:
            if value.count("'") == 2:
                value = value[1:-1]
                sys.argv[index] = value
            if index != 1:
                sys.argv.insert(1, sys.argv.pop(index))
            return True
    return False


def check_if_url_or_date_in_arguments() -> str:
    """Checks if url in args and puts it to sys.argv[1] else raises exception"""
    flag = check_if_help_or_version_in_arguments()
    if not flag:
        if not check_if_date_in_arguments():
            if link_found():
                return 'link_only'
            else:
                raise custom_error.UrlNotFoundInArgsError
        else:
            if link_found():
                return 'link_and_date'
            else:
                return 'date_only'
    else:
        return flag


def check_the_connection(rss_url: str) -> None:
    """Checks the connection"""
    try:
        urllib.request.urlopen(rss_url)
    except urllib.request.HTTPError as e:
        info = f'{e.code}: {e.reason}'
        raise custom_error.ConnectionFailedError(f"Connection failed: {info}")
    except urllib.request.URLError as e:
        info = f'{e.reason}'
        raise custom_error.ConnectionFailedError(f"Connection failed: {info}")


def check_if_url_is_valid(rss_url: str) -> bool:
    """Checks if link is valid"""
    try:
        result = urllib.request.urlparse(rss_url)
        return all([result.scheme, result.netloc, "." in result.netloc, len(result.netloc) > 2])
    except ValueError:
        return False


def valid_url(rss_url: str) -> str:
    """Checks if url is valid and connection successful"""
    if check_if_url_is_valid(rss_url):
        logging.info('Valid url')
        check_the_connection(rss_url)
        logging.info('Connection successful')
        return rss_url
    else:
        msg = f"Not a valid URL value: '{rss_url}'"
        raise custom_error.NotValidUrlError(msg)


def valid_limit(limit: str) -> Optional[int]:
    """Checks if limit is valid"""
    try:
        limit = int(limit)
        if (limit is None) or (limit > 0):
            return limit
        else:
            msg = f"Not a valid limit value: '{limit}'"
            raise custom_error.NotValidLimitError(msg)
    except ValueError:
        msg = f"Invalid int value: '{limit}'"
        raise custom_error.NotValidLimitError(msg)


def valid_date(date: str) -> datetime.datetime:
    """Checks if date is valid"""
    try:
        if len(str(date)) != 8:
            msg = f'Date must be 8 digits (yyyymmdd)'
            raise custom_error.NotValidDateError(msg)
        else:
            return datetime.datetime.strptime(date, "%Y%m%d")
    except ValueError:
        msg = f"Not a valid date: '{date}'"
        raise custom_error.NotValidDateError(msg)


def valid_directory_path(path: str, key: str) -> str:
    """Checks if path is valid"""
    if path[-1] != "\\":
        path += "\\"

    if os.path.isdir(path):
        if key == 'html':
            filename = 'NEWS.html'
        else:
            filename = 'NEWS.pdf'
        full_name = os.path.join(path, filename)
        return full_name
    else:
        raise custom_error.NotValidPathError(f'Not valid path to {key}: {path}')


def valid_directory_html(path: str) -> str:
    """Checks if path is valid"""
    return valid_directory_path(path, 'html')


def valid_directory_pdf(path: str) -> str:
    """Checks if path is valid"""
    return valid_directory_path(path, 'pdf')


def create_parser(checker: str) -> argparse.ArgumentParser:
    """Adding arguments to run the application"""
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    if checker != 'link_and_date':
        if checker == 'full':
            parser.add_argument("source", type=valid_url, help="RSS URL")
    else:
        parser.add_argument("source", type=str, help="RSS URL")

    parser.add_argument("--version", action='version', version=f'%(prog)s version: {VERSION}',
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=valid_limit, default=None, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=valid_date,
                        help="Prints the cashed news from the specified day. Format - %%Y%%m%%d")
    parser.add_argument("--to-html", type=valid_directory_html,
                        help="Converts news to html")
    parser.add_argument("--to-pdf", type=valid_directory_pdf,
                        help="Converts news to pdf")
    return parser
