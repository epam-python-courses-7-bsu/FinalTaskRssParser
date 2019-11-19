"""Contain parsing and text processing functions"""


import feedparser
from lxml import etree
import datetime
import argparse
from classes.news_class import News
from functions.check_func import check_feed_status


def parse_date(date_time_str):
    """Turn date string argument into datetime object

    Uses inside get_arguments function
    """
    try:
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y%m%d')
        str_date = date_time_obj.strftime("%d %b %Y")
        return str_date
    except ValueError as E:
        raise argparse.ArgumentTypeError(E)


def get_arguments(parser):
    """Getting command-line arguments"""

    parser.add_argument('--version', action='version', version='rss-reader 5.7')
    parser.add_argument("--json", help="Print result as JSON in stdout",
                        action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages",
                        action="store_true")
    parser.add_argument("--limit", help="""Limit news topics if this parameter
                        provided""", type=int)
    parser.add_argument("--date", help="""Take a date in %%Y%%m%%d format.
                        Print cached news, published on this date. 
                        If source argument passed, print only news from this source""", type=parse_date)
    parser.add_argument("--to-epub", help="""Create a book in epub format from internet
                        source or database. Receive the path where file will be saved""", type=str, default='')
    parser.add_argument("--to-html", help="""Create a file in html format from internet
                        source or database. Receive the path where file will be saved""", type=str, default='')
    parser.add_argument("source", help="RSS URL", nargs='?', default='')
    parser.add_argument("--colorize", action="store_true", help="Print the result of the utility in colorized mode")
    command_line_args = parser.parse_args()
    return command_line_args


def parse_feed(command_line_args, logger):
    """Get feed by url using feedparser"""

    logger.info("Parsing feeds...")
    url = command_line_args.source
    feed = feedparser.parse(url)
    feed = check_feed_status(feed)
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

    Function uses inside process_feed() function.
    Return tuple of lists ([href_links], [img_links])
    """
    list_of_href_links = []
    list_of_img_links = []

    # find href and img links
    href_links = root.xpath('.//a/@href')
    img_links = root.xpath('.//img/@src')

    # Add links in list of links
    list_of_href_links.extend(href_links)
    list_of_img_links.extend(img_links)

    return (list_of_href_links, list_of_img_links)


def process_feed(command_line_args, feed, logger):
    """
    Get feed title
    Create a list of news instance objects
    """
    # Get feed title and source of feed
    feed_title = feed.feed.get("title", "")
    source = command_line_args.source

    # Process of entries in feed
    news_collection = []
    logger.info("Creating a collection of news...")
    for num, entry in enumerate(feed.entries):
        logger.info("Collected {}".format(num+1))

        # Process description
        description = entry.get("description", "")
        root = get_xml_root(description)
        text = extract_text_from_description(root)
        links = extract_links_from_description(root)

        # Get title, date, link from entry
        title = entry.get("title", "").replace('&#39;', "'")
        date = entry.get("published", "")
        link = entry.get("link", "")

        # Create News object
        news = News(title, date, link, text, links, feed_title, source, command_line_args)

        # Adding news entry in the collection
        news_collection.append(news)

    return news_collection
