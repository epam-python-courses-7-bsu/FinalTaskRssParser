import re
import json
from FinalTaskRssParser.final_task.rss_reader.data.RSSFeed import Feed
from FinalTaskRssParser.final_task.rss_reader.data.RSSItem import Item
from FinalTaskRssParser.final_task.exceptions.exception_handler import ExceptionHandler


class RSSDataHandler:
    """
    Get's data from rss_parser and converts it into needed format
    """

    def __init__(self, feed, entries, json_flag, limit):
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

        if json_flag:
            self.json_data = self.to_json()
        else:
            self.json_data = None

    def to_json(self):
        data = dict()

        data['feed'] = {
            "title": self.feed.title,
            "description": self.feed.description,
        }
        data['items'] = list()

        for i, element in enumerate(self.entries):
            data['items'].append({'title': element.title})
            data['items'].append({'link': element.link})
            for links in element.image_links:
                data['items'].append({'image_links': links.get('href')})
            data['items'].append({'description': element.description})
            data['items'].append({'pub_date': element.pub_date})

            if i + 1 == self.limit:
                break

        return json.dumps(data, indent=2)

    def get_entries(self) -> list:
        if not self.limit:
            out = self.entries
        elif self.limit > 0:
            out = self.entries[:self.limit]
        else:
            raise ExceptionHandler
        return out


# Delete unnecessary content from description
def description_handler(string: str) -> str:
    clean = re.compile("<.*?>")
    description = re.sub(clean, '', string)
    return description
