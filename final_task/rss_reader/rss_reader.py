import sys
import os
import argparse
import logging
dir_add = os.path.abspath(os.path.dirname(__file__))
sys.path.append(dir_add)
from RSSReader import RSSReader


VERSION = '5.0'


def arg_parse(args):
    """Function which parsed command-line arguments."""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument("source", type=str, nargs='?',
                        help="RSS URL")
    parser.add_argument("--limit", type=int,
                        help="Limit news topics if this parameter provided")
    parser.add_argument("--version", action="store_true",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    parser.add_argument("--date", type=str,
                        help="Return news from cache with that date")
    parser.add_argument("--to_pdf", type=str,
                        help="Conversion of news in the pdf format")
    parser.add_argument("--to_epub", type=str,
                        help="Conversion of news in the epub format")
    parser.add_argument("--colorize", action="store_true",
                        help="Print news in colorized mode in stdout")
    return parser.parse_args(args)


def main():
    args = arg_parse(sys.argv[1:])
    level = logging.INFO if args.verbose else logging.ERROR
    logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s', stream=sys.stdout, level=level)
    if args.version:
        print('RSS-reader version {}'.format(VERSION))  # program version call
        return
    reader = RSSReader(args.date, args.source, args.limit, args.json, args.to_pdf, args.to_epub, args.colorize)
    reader.get_news()


if __name__ == '__main__':
    main()
