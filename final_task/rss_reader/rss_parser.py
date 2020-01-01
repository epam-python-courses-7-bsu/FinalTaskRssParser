from exceptions import *
from Logger import Logger
from feedparser import parse
import feedparser


def rss_handler(url: str) -> tuple or None:
    """Download RSS from the web"""
    logger = Logger().get_logger(__name__)
    logger.info("Attempt to follow the link...")

    try:
        rss_data = parse(url)
        if rss_data.bozo:
            logger.error("Parsing failed...")
            raise ContentTypeException# rss_data.bozo_exception

    except ContentTypeException:
        logger.error("Parsing failed...\n"
                    "Can't parse RSS from this site:\n"
                    "Feeds isn't well-formed")

    else:
        logger.info("Parsing passed correctly")
        return rss_data.feed, rss_data.entries

    logger.error("Parsing failed...")
    return None
