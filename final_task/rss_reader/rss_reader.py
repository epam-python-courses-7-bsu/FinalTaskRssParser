import argparse
from typing import Union
import feedparser
import logging
import json
import sys
from rss_reader.work_with_file import read_feed_form_file
from rss_reader.work_with_file import add_feed_to_file
from rss_reader.work_with_text import get_string_with_result
from rss_reader.work_with_json import to_json
from rss_reader.work_with_json import limited_json
from rss_reader.decorators import functions_log
from rss_reader import __version__


@functions_log
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
    args = parser.parse_args()
    if not args.limit:
        args.limit = 1000
    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p',
                            stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p',
                            filename="sample.log", level=logging.DEBUG)
    return args


def run():
    args = set_start_setting()
    logging.info('the application is running')
    logging.debug('args: ' + str(args))
    if args.version:
        print(f'RSS reader version {__version__}')
    elif args.date:
        data = read_feed_form_file(args.date)
        if args.json:
            data = limited_json(data, args.limit)
            print(json.dumps(data, ensure_ascii=False))
        else:
            print(get_string_with_result(data, args.limit))
    elif args.source:
        data = get_object_feed(args.source)
        data = to_json(data)
        if 'error' not in data:
            add_feed_to_file(data)
        if args.json:
            data = limited_json(json.loads(data), args.limit)
            print(json.dumps(data, ensure_ascii=False))
        else:
            print(get_string_with_result(json.loads(data), args.limit))
    else:
        print('How work with application?\nEnter in command line: rss-reader -h')
    logging.info('the application is finished')


if __name__ == '__main__':
    run()
