import argparse

def arguments():
    """create command line arguments"""

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    # source url
    parser.add_argument(
        'source',
        type=str,
        help='RSS URL'
    )
    # version
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0',
        help='Print version info'
    )
    # json format
    parser.add_argument(
        '--json',
        action='store_true',
        help='Print result as JSON in stdout'
    )
    # verbose (logs)
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Outputs verbose'
    )
    # topic limit
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit news topics'
    )
    return parser.parse_args()
    