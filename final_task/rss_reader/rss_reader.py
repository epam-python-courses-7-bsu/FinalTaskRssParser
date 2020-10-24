import CLI
from data import RSSDataHandler
from html import unescape
from Logger import Logger
import os
from output_handler import OutputHandler
from pprint import pprint
from rss_parser import rss_handler
import sys


def main():
    """Start point of the program"""

    # Parse arguments from command line
    cl_args = CLI.parse()

    # Prints version of rss_reader and directory where it's placed
    if cl_args.get('version'):
        print(f"RSS-Reader {version}" + " from " + str(os.getcwd()))
        sys.exit()

    # Allow logger to print logs to command-line
    Logger().set_stream_logging(cl_args.get('verbose'))

    # Create logger by implemented function
    logger = Logger().get_logger("rss_reader")

    data = RSSDataHandler(*rss_handler(cl_args.get('source')), cl_args.get('json'), cl_args.get('limit'))

    output = OutputHandler(data, cl_args.get('colorize'))
    if cl_args.get('json'):
        pprint(unescape(output.format_to_json_string()))
    else:
        for text in output.format_news():
            print(text, end="\n\n")


if __name__ == '__main__':
    version = '0.2'     # Version of the program
    main()
