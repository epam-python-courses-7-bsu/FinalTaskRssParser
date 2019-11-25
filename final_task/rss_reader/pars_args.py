import argparse
import sys
import logging

MODULE_LOGGER = logging.getLogger("rss_reader.pars_args")


def create_parser():
    """ function to parse the command line """
    logger = logging.getLogger("rss_reader.create_parser")
    logger.info("parse the command line ")
    parser = argparse.ArgumentParser(
        prog='rss_reader',
        description=''' This program receives RSS URL 
                        and prints results in human-readable format.''',
        epilog='''Thank you for using this program'''

    )

    # add information about the expected parameters
    # using the add_argument method one call for each parameter).

    parser.add_argument('source', type=str, nargs='?', default="", help='RSS URL')

    parser.add_argument('--version', action='version', help='Print version info', version=f'{5.0}')

    parser.add_argument('--json', action='store_const', const=True, default=False,
                        help='Print result as JSON in stdout')

    parser.add_argument('--verbose', action='store_const', const=True, default=False,
                        help='Outputs verbose status messages')

    parser.add_argument('--limit', type=int, metavar='LIMIT', default=None,
                        help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, metavar='DATE',
                        help='to search in cache for news by date in the format in YYYYmmdd')
    parser.add_argument('--to-html', type=str, metavar='PATH', default=None,
                        help='the conversion of news in html file')
    parser.add_argument('--to-pdf', type=str, metavar='PATH', default=None,
                        help='the conversion of news in pdf file')
    parser.add_argument('--colorize', action='store_const', const=True, default=False,
                        help='print news in multi colored format')
    parser.add_argument('--clear', action='store_const', const=True, default=False,
                        help='Clears news story')
    return parser


def get_args():
    """
      returns command line arguments
    """
    logger = logging.getLogger("rss_reader.get_args")
    logger.info("return args  command line")
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    return args
