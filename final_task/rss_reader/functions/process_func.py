"""Contain parsing and text processing functions

Functions
---------
parse_feed(command_line_args, logger) -> feed
    Get feed by url using feedparser
--------------------------------------------
get_xml_root(xml_file) -> root
    Create lxml parser, return root of xml file.
    Function uses inside process_feed() function
--------------------------------------------
extract_text_from_description(root)-> text
    Extract text from description root
    Function uses inside process_feed() function
--------------------------------------------
extract_links_from_description(root):
    Extract links from description
    Function uses inside process_feed() function
--------------------------------------------
process_feed(feed, logger) -> news_collection
    Get feed title
    Create a list of news instance objects
"""


import feedparser
from lxml import etree
from classes.news_class import News
import functions.check_func as ch_f


def parse_feed(command_line_args, logger):
    """Get feed by url using feedparser"""

    logger.info("Parsing feeds...")
    url = command_line_args.source
    feed = feedparser.parse(url)
    feed = ch_f.check_feed_status(feed, logger)
    return feed


def get_xml_root(xml_file):
    """Create lxml parser, return root of xml file

    Function uses inside process_feed() function
    """

    # Create lxml parser
    parser = etree.HTMLParser(remove_blank_text=True)
    # Get root of description tree
    root = etree.fromstring(xml_file, parser)
    return root


def extract_text_from_description(root):
    """Extract text from description root

    Function uses inside process_feed() function
    """

    # Get text from description tree
    list_of_text = root.xpath("//text()")
    # Turn list of strings into string
    text = ''.join(list_of_text)
    return text


def extract_links_from_description(root):
    """Extract links from description

    Function uses inside process_feed() function
    """

    list_of_links = []
    # find href and img links
    href_links = root.xpath('.//a/@href')
    img_links = root.xpath('.//img/@src')
    # Add links in list of links
    list_of_links.extend(href_links)
    list_of_links.extend(img_links)
    # Turn a list of links to a pretty formating string
    string_repr_of_links = ''
    for num, link in enumerate(list_of_links):
        string_repr_of_links = string_repr_of_links + '[{}] '.format(num+1) + link + '\n'
    return string_repr_of_links


def process_feed(feed, logger):
    """
    Get feed title
    Create a list of news instance objects
    """

    # Get feed title and set feed_title attribute to News()
    feed_title = feed.feed.get("title", "")
    News.feed_title = feed_title

    # Process of entries in feed
    news_collection = []
    logger.info("Creating a collection of news...")
    for entry in feed.entries:
        # Process description
        description = entry.get("description", "")
        root = get_xml_root(description)
        text = extract_text_from_description(root)
        links = extract_links_from_description(root)

        # Create News object and define attributes
        news = News()
        news.title = entry.get("title", "").replace('&#39;', "'")
        news.date = entry.get("published", "")
        news.link = entry.get("link", "")
        news.text = text
        news.links = links
        # Adding news entry in the collection
        news_collection.append(news)
    return news_collection
