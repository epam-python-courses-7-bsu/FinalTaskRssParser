import sys
import argparse
import logging
from final_task.rss_reader import rss_reader


__version__ = '1.0'


if __name__ == '__main__':
    """This is executed when run from the command line"""
    try:
        parser = argparse.ArgumentParser(description='Some description')
        # Required position argument
        parser.add_argument('source', type=str, help='RSS URL')
        # Specify output of "--version"
        parser.add_argument('--version', action='version', version='%(prog)s Iteration {version}'.format(version=__version__), help='Print version info')
        # Optional argument
        parser.add_argument('--json', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                            help='Print result as JSON in stdout')
        # Optional argument limit count of news
        parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
        args = parser.parse_args()
        limit = args.limit
        source = args.source
        logging.basicConfig(filename='rss_logging.log', level=logging.INFO)
        logging.info('return limit news')
        print(rss_reader.get_news(source)['News'][:limit])
        logging.info('return limit news')
    except (TypeError, ValueError, IndexError):
        sys.exit("Error limit")
