from console_interface import parse_args
import logging
import sqlite3
from rss_parser import *
from console_interface import get_args


def main():
    args = parse_args()
    dict_of_args = get_args(args)
    logging.debug("Check in main")
    try:
        if dict_of_args.get("date"):
            print_cache(dict_of_args)
        else:
            parse(dict_of_args)
    except sqlite3.OperationalError:
        print("Something wrong with database")
    except OSError:
        print("Some problems")
        logging.error(OSError)
        logging.error("File can't be opened")
    except Exception:
        print("Sorry, for some reason the app can't work")


if __name__ == '__main__':
    main()
