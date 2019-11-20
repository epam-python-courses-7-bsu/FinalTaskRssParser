from rss_parser import RssParser
from console_interface import ConsoleInterface
import logging

def main():
    console = ConsoleInterface()
    logging.debug("Check in main")
    rssobject = RssParser(console.source, console.limit, console.json)

if __name__ == '__main__':
    main()