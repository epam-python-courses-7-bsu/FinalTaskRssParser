import argparse

class ComLineArgParser:
    """Class for parsing arguments from command-line interface

    Class creates an instance of ArgumentParser(), gets arguments
    and contains all passed arguments like attributes.
    """
    def get_arguments(self):
        """Getting command-line arguments"""
        # Creating ArgumentParser() instance
        parser = argparse.ArgumentParser()
        # Adding arguments and set preferences
        parser.add_argument("--version", help="Print version info",
                            action="store_true")
        parser.add_argument("--json", help="Print result as JSON in stdout",
                            action="store_true")
        parser.add_argument("--verbose", help="Outputs verbose status messages",
                            action="store_true")
        parser.add_argument("--limit", help="""Limit news topics if this parameter
                            provided""", type=int)
        parser.add_argument("source", help="RSS URL")
        # Parse arguments
        args = parser.parse_args()
        return args

    def __init__(self):
        """Store all arguments as class attributes"""

        args = self.get_arguments()

        self.version = args.version
        self.json = args.json
        self.verbose = args.verbose
        self.limit = args.limit
        self.source = args.source
