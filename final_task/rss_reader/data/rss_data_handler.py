import exceptions
from Logger import Logger
import re
from .RSSFeed import Feed
from .RSSItem import Item


class RSSDataHandler:
    """
        Get's data from rss_parser and converts it into needed format
    """

    def __init__(self, feed, entries, is_json_generated, limit):
        self.limit = limit
        self.feed = Feed(feed.get("title"), description_handler(feed.get("description")))
        self.entries = list()

        for element in entries:
            self.entries.append(
                Item(element.get("title"),
                     element.get("link"),
                     element.get("links"),
                     description_handler(element.get("summary_detail").get("value")),
                     element.get("published")
                     ))

    def create_data_dict(self):
        logger = Logger().get_logger(__name__)
        logger.info("Converting to JSON...")
        data_dict = dict()

        data_dict['feed'] = {
            "title": self.feed.title,
            "description": self.feed.description,
        }
        data_dict['items'] = list()

        for element in self.entries:
            data_dict['items'].append({'title': element.title})
            data_dict['items'].append({'link': element.link})
            for links in element.image_links:
                data_dict['items'].append({'image_links': links.get('href')})
            data_dict['items'].append({'description': element.description})
            data_dict['items'].append({'pub_date': element.pub_date})

        data_dict['items'] = data_dict['items'][:self.limit]

        return data_dict

    def get_entries(self) -> list:
        if not self.limit:
            out = self.entries
        elif self.limit > 0:
            out = self.entries[:self.limit]
        else:
            raise exceptions.LimitException
        return out


# Delete unnecessary content from description
def description_handler(string: str) -> str:
    clean = re.compile("<.*?>")
    description = re.sub(clean, '', string)
    return description
