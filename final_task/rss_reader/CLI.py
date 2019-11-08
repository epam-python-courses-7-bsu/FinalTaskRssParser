import argparse as arp
from test import urls


class ArgParser:
    """Parsing arguments from command line"""
    def __init__(self):
        self.parser = arp.ArgumentParser("RSS parser")
        self.parser.add_argument("-V", "--version", help='Print version info', action='store_true')
        self.parser.add_argument("--json", help='Prints result into JSON in stdout', action='store_true')
        self.parser.add_argument("-v", "--verbose", help='Outputs verbose status messages', action='store_true')
        self.parser.add_argument('--limit', type=int, help='Limit the news topics if this parameter provided')
        self.parser.add_argument('source', type=str, help='RSS URL')
        self.arguments = dict()

    def parse(self):
        self.arguments = vars(self.parser.parse_args())
        return self.arguments
