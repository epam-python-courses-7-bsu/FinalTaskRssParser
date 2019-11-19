from FinalTaskRssParser.final_task.rss_reader.data.RSSFeed import Feed
from FinalTaskRssParser.final_task.rss_reader.data.RSSItem import Item
from FinalTaskRssParser.final_task.exceptions.exception_handler import ExceptionHandler


class RSSDataHandler:
    def __init__(self, feed, entries):
        self.feed = Feed(feed.get("title"), feed.get("description"))
        self.entries = list()
        for i, element in enumerate(entries):
            self.entries.append(
                Item(element.get("title"),
                     element.get("link"),
                     element.get("link"),
                     element.get("description"),
                     element.get("published")
                     ))
        self.size = len(self.entries)

    @property
    def get_entries(self, limit=0) -> list:
        if not limit:
            out = self.entries
        elif limit > 0:
            out = self.entries[:limit]
        else:
            raise ExceptionHandler
        return out

    @property
    def get_feed(self):
        return self.feed
