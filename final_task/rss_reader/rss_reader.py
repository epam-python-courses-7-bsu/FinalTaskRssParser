from rss_parser import RssParser
import psycopg2
from console_interface import ConsoleInterface
import logging

def main():
    console = ConsoleInterface()
    logging.debug("Check in main")
    try:
        rssobject = RssParser(console.source, console.limit, console.json, console.date, console.path, console.to_html)
    except psycopg2.OperationalError:
        print("Something wrong with database")

if __name__ == '__main__':
    main()