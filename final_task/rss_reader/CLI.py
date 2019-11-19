import argparse as arp


def parse():
    """Parsing arguments from command line"""
    parser = arp.ArgumentParser("RSS parser")
    parser.add_argument("-V", "--version", help='Print version info', action='store_true')
    parser.add_argument("--json", help='Prints result into JSON in stdout', action='store_true')
    parser.add_argument("-v", "--verbose", help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', type=int, help='Limit the news topics if this parameter provided')
    parser.add_argument('source', type=str, help='RSS URL')

    """Arguments - dict of arguments parsed from command line"""
    arguments = vars(parser.parse_args())   # Get arguments from command line and puts them into dict self.arguments

    return arguments
