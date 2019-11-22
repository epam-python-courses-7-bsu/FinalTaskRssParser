import argparse


def arguments():
    """create command line arguments"""

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose')
    parser.add_argument('--limit', type=int, help='Limit news topics')
    parser.add_argument('--date', type=str, help='Read news from given date')
    parser.add_argument('--to_html', action='store_true', help='Save feed in html format')
    parser.add_argument('--to_pdf', action='store_true', help='Save feed in pdf format')
    return parser.parse_args()
