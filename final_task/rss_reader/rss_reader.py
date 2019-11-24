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
import work_with_colorize
import RssReaderException
import work_with_feedparser
import __init__


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
    parser.add_argument("--colorize", help="Colorize text", action="store_true")
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
    args = set_start_setting()
    logging.info('the application is running')
    logging.debug('args: ' + str(args))
    logging.info(os.getcwd())
    data = None
    try:
        if args.version:
            pass
        elif args.date:
            data = work_with_file.read_feed_form_file(args.date)
        elif args.source:
            data = work_with_feedparser.get_object_feed(args.source)
            data = work_with_dict.to_dict(data)
            work_with_file.add_feed_to_file(data)
        else:
            raise RssReaderException.RssReaderException('How work with application?\nEnter in command line: rss-reader -h')

        if args.version:
            result = f'RSS reader version {open("VERSION.txt").readline()}'
        else:
            if args.limit:
                data = work_with_dict.limited_dict(data, args.limit)
            if args.json:
                result = json.dumps(data, ensure_ascii=False, indent=4)
            elif args.to_html:
                result = work_with_html.write_to_html_file(data, args.to_html)
            elif args.to_pdf:
                result = work_with_pdf.write_to_pdf_file(data, args.to_pdf)
            elif args.colorize:
                result = work_with_colorize.colorize_text(data)
            else:
                result = work_with_text.get_string_with_result(data, args.limit)
        print(result)
    except RssReaderException.RssReaderException as exc:
        print(exc.expression)
        print(exc)
    logging.info('the application is finished')


if __name__ == '__main__':
    run()