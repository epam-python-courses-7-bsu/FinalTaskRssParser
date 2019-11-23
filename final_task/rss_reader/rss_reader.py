import argparse
import logging

from feed import Feed, URLFormatError, FeedNotFoundError, IncorrectRSSError

# temp
__version__ = "0.1"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", action="version", version=f"{parser.prog}s {__version__}",
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

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
        feed = Feed(rss_url, limit)
    except (URLFormatError, FeedNotFoundError, IncorrectRSSError) as e:
        logging.error(str(e))
    else:
        if not args.json:
            print(feed.render_text())
        else:
            print(feed.render_json())

    logging.info("Program finishes")
