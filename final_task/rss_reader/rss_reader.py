import argparse
from typing import Union
import feedparser
import logging
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


import work_with_file
import work_with_text
import work_with_dict
import work_with_html
import work_with_pdf
import decorators
import __init__


@decorators.functions_log
def get_object_feed(url: str) -> Union[str, feedparser.FeedParserDict]:
    try:
        data = feedparser.parse(url)
        if data.status == 200:
            if data.bozo:
                return f'ERROR: There is no rss feed at this url: {url}'
            else:
                return data
        else:
            return f'HTTP Status Code {data.status}'
    except AttributeError:
        return f'ERROR: {url} - is not url(example url "https://google.com")'
    except Exception as exc:
        return f'ERROR: {exc}'


def set_start_setting():
    """setup start settings"""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL", nargs='?', default='', type=str)
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("--date", help="Obtaining the cached news without the Internet", type=str)
    parser.add_argument("--to-html", help="The argument gets the path where the HTML news will be saved", type=str)
    parser.add_argument("--to-pdf", help="The argument gets the path where the PDF news will be saved", type=str)
    args = parser.parse_args()
    if not args.limit:
        args.limit = -1
    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p',
                            stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p',
                            filename="sample.log", level=logging.DEBUG)
    return args


def run():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print(os.getcwd())
    args = set_start_setting()
    logging.info('the application is running')
    logging.debug('args: ' + str(args))
    data = None
    if args.version:
        print(f'RSS reader version {__init__.VERSION}')
    elif args.date:
        data = work_with_file.read_feed_form_file(args.date)
    elif args.source:
        data = get_object_feed(args.source)
        data = work_with_dict.to_dict(data)
        if 'error' not in data:
            work_with_file.add_feed_to_file(data)
    else:
        print('How work with application?\nEnter in command line: rss-reader -h')
        exit(1)

    logging.debug(type(data))
    logging.debug(data)
    if args.limit:
        data = work_with_dict.limited_dict(data, args.limit)
    if data.get('error', False):
        print(data['error'])
    elif args.json:
        print(json.dumps(data, ensure_ascii=False, indent=4))
    elif args.to_html:
        work_with_html.write_to_html_file(data, args.to_html)
    elif args.to_pdf:
        work_with_pdf.write_to_pdf_file(data, args.to_pdf)
    else:
        print(work_with_text.get_string_with_result(data, args.limit))
    logging.info('the application is finished')


if __name__ == '__main__':
    run()