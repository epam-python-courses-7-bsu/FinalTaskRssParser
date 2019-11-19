from FinalTaskRssParser.final_task.rss_reader.logs import Logger
import feedparser
from feedparser import parse


def rss_handler(url: str) -> tuple or None:
    """Download RSS from the web"""
    logger = Logger().get_logger(__name__)
    logger.info("Attempt to follow the link...")

    try:
        rss_data = parse(url)
        if rss_data.bozo:
            logger.error("Parsing failed...")
            raise rss_data.bozo_exception

    except feedparser.NonXMLContentType:
        logger.error("Parsing failed...\n"
                    "Can't parse RSS from this site:\n"
                    "Feeds isn't well-formed")

    else:
        logger.info("Parsing passed correctly")
        return rss_data.feed, rss_data.entries

    logger.error("Parsing failed...")
    return None
