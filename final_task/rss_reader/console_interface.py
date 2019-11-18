import argparse
import logging

class ConsoleInterface():
    """ Implement console interface"""

    source = ""
    limit = -1
    version = "Version 1.1"
    json = False
    verbose = False

    def __init__(self):
        """ Gets parametres from console"""

        parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
        parser.add_argument("source", help="RSS url")
        parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
        parser.add_argument("--version", action="store_true", help="Print version info")
        parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
        parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")

        args = parser.parse_args()


        self.source = args.source
        if args.limit:
            self.limit = args.limit
        if args.version:
            print(self.version)
        if args.json:
            self.json = True
        if args.verbose:
            self.verbose = True
            logging.basicConfig(level=logging.DEBUG, format='%(process)d-%(levelname)s-%(message)s')
        else:
            logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        logging.debug("Check in interface")
