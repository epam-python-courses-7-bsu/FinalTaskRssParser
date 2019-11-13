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
    logging.info('Getting RSS from ' + rss_url)
    parser = feedparser.parse(rss_url)

    if parser.bozo:
        raise GettingRSSException(str(parser.bozo_exception))

    logging.debug('limit = ' + str(limit))
    if limit:
        logging.info('Cutting item list.')
        parser.entries = parser.entries[:limit]

    return parser


class GettingRSSException(Exception):
    def __init__(self, msg):
        super().__init__('Problems with getting RSS: ' + msg)


def format_description(description):
    """ Format 'description' tag.

    Retrieves images' links and replace all 'img' tags to construction [image_name][image_number].

    :param description: description tag with his content
    :type description: str

    :return: content of formatted description and list of image links
    :rtype: tuple of: str and list of str
    """
    if isinstance(description, str.__class__):
        raise TypeError(f'Wrong type: {type(description)}. Expected type of description: {str}')

    logging.info('Creating description soup.')
    description_soup = BeautifulSoup(description, 'html.parser')
    links = list()

    logging.info('Replacing img tags and extracting links.')
    for num, img in enumerate(description_soup.find_all('img')):
        if img['src']:
            links.append(img['src'])
            img.replace_with(f'[image {num+1}: {img["alt"]}][{num+1}]')

    return description_soup.text, links
