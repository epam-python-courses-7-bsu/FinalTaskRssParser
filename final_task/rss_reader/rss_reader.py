import sys
import argparse
from RSSReader import RSSReader


VERSION = '2.0'


def arg_parse(args):
    """Function which parsed command-line arguments."""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument("source", type=str,
                        help="RSS URL")
    parser.add_argument("--limit", type=int,
                        help="Limit news topics if this parameter provided")
    parser.add_argument("--version", action="store_true",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    return parser.parse_args(args)


def main():
    args = arg_parse(sys.argv[1:])
    if args.version:
        print('RSS-reader version {}'.format(VERSION))  # program version call
        return
    reader = RSSReader(args.source, args.verbose)
    reader.limit = args.limit
    reader.is_json = args.json
    reader.get_news()


if __name__ == '__main__':
    main()
