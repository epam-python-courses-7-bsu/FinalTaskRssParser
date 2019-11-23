from rss_parser import RssParser
from console_interface import parse_args
import logging
import sqlite3
from console_interface import get_args

def main():
    args = parse_args()
    list_of_args = get_args(args)
    logging.debug("Check in main")
    try:
        rssobject = RssParser(list_of_args[0], list_of_args[1], list_of_args[2], list_of_args[3],
                              list_of_args[4], list_of_args[5], list_of_args[6])
    except sqlite3.OperationalError:
        print("Something wrong with database")
    except OSError:
        print("Some problems")
        logging.error(OSError)
        logging.error("File can't be opened")

if __name__ == '__main__':
    main()