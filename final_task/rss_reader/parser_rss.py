import feedparser
import logging
from bs4 import BeautifulSoup


def create_feedparser(rss_url, limit=0):
    """ Create feedparser with limited number of items or all items.

    If limit value is not set or =0 or =None created feedparser with all items.
    Otherwise created feedparser with limit value items.

    :param rss_url: url of RSS
    :type rss_url: str

    :param limit: count of items
    :type limit: int

    :raise Exception: if there are problems with getting rss

    :return: feedparser
    :rtype: 'feedparser.FeedParserDict'
    """
    parser = feedparser.parse(rss_url)

    if parser.bozo:
        raise Exception('Problems with getting RSS: ' + str(parser.bozo_exception))

    if limit:
        parser.entries = parser.entries[:limit]

    return parser


def format_description(description):
    """ Format 'description' tag.

    Retrieves images' links and replace all 'img' tags to construction [image_name][image_number].

    :param description: description tag with his content
    :type description: str

    :return: content of formatted description and list of image links
    :rtype: tuple of: str and list of str
    """
    if not type(description) == str:
        raise TypeError(f'Wrong type: {type(description)}. Expected type of description: {str}')

    description_soup = BeautifulSoup(description, 'html.parser')
    links = list()

    for num, img in enumerate(description_soup.find_all('img')):
        links.append(img['src'])
        img.replace_with(f'[image {num+1}: {img["alt"]}][{num+1}]')

    return description_soup.text, links


def log():
    logging.basicConfig(level=logging.DEBUG)
