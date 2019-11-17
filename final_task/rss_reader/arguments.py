import argparse


version = '4.0'

""" Add argument commands for script """


def command_line():

    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.',
        prog='rss-reader')

    parser.add_argument(
        'URL',
        action="store",
        help='rss url')

    parser.add_argument(
        '--version',
        action='version',
        help='info about version',
        version='%(program)s {}'.format(version))

    parser.add_argument(
        '-j', dest='json',
        help='print result as json in stdout',
        action='store_true')

    parser.add_argument(
        '--verbose',
        dest="verbose",
        help="print lots of debugging statements",
        action="store_true")

    parser.add_argument(
        '--lim',
        dest='limit',
        type=int,
        help='limit news topics if this parameter provided')

    parser.add_argument(
        '--log',
        dest='log_level',
        type=int,
        help='limit news topics if this parameter provided')

    parser.add_argument(
        '--date',
        action='store',
        help='print news from the specified day')

    parser.add_argument(
        '--html',
        action='store',
        help='convert news in html format')

    parser.add_argument(
        '--pdf',
        action='store',
        help='convert news in pdf format')
    return parser.parse_args()
