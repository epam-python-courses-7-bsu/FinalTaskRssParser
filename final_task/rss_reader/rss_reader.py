import argparse
import logging
import time

from . import feed

# temp
__version__ = "0.3"
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

    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", action="version", version=f"{parser.prog}s {__version__}",
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
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
            if not args.json:
                print(rss_feed.render_text())
            else:
                print(rss_feed.render_json())
    except feed.FeedError as e:
        logging.error(str(e))

    logging.info("Program finishes")
