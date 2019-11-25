import argparse
import logging
import time
import os.path

from . import feed

# temp
__version__ = "0.4"
PROG = "rss-reader"
DATE_FORMAT = "%Y%m%d"


def date_str(string):
    logging.info("Checking date argument")
    try:
        date = time.strptime(string, DATE_FORMAT)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Incorrect date format: {string}")
    return date


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.", prog=PROG)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    group.add_argument("--html", type=str, help="Generate html book on path", metavar='PATH')
    group.add_argument("--epub", type=str, help="Generate epub book an path", metavar='PATH')

    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", action="version", version=f"{parser.prog}s {__version__}",
                        help="Print version info")
    # parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

    # It is done because argparse treat '%' in parameters as old-style formatting
    date_format_escaped = DATE_FORMAT.replace("%", "%%")
    parser.add_argument("--date", type=date_str,
                        help=f"Load news with date ({date_format_escaped}) from cache, if this parameter provided")

    args = parser.parse_args()

    rss_url = args.source

    if args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    limit = args.limit if args.limit is not None else 0
    logging.basicConfig(format="%(levelname)s:%(message)s", level=log_level)

    logging.info("Program starts")

    try:
        with feed.Feed(rss_url, limit, date=args.date) as rss_feed:
            if args.json:
                print(rss_feed.render_json())
            elif args.epub is not None:
                rss_feed.create_epub(args.epub)
            elif args.html is not None:
                rss_feed.create_html(args.html)
            else:
                print(rss_feed.render_text())
    except feed.FeedError as e:
        logging.error(str(e))

    logging.info("Program finishes")
