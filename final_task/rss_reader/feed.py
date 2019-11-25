import urllib.parse
import html
import json
import logging
import time
import feedparser

from . import html_to_text
from .database import DB, DBError


class URLFormatError(ValueError):
    pass


class FeedNotFoundError(Exception):
    pass


class IncorrectRSSError(Exception):
    pass


class LocalCacheError(Exception):
    pass


class Feed:

    def __init__(self, link, limit=0, *, date=None):
        self.link = self._try_fix_url(link)
        logging.info(f'The link to the rss feed is "{self.link}"')
        self.title = None
        self.items = []

        self.limit = int(limit)
        self.date = date
        try:
            self.db = DB()
        except DBError:
            if self.date is not None:
                raise LocalCacheError("Unable to open local cache")
            else:
                self.db = None
                logging.warning("Unable to open local cache. Feed items will not be saved.")

        if date is None:
            self._parse_remote()
            self._save_to_cache()
        else:
            self.date = date
            self._load_cache()

    def _parse_remote(self):
        logging.info("Parsing feed from remote source")
        parsed_rss = feedparser.parse(self.link)
        # Did Feedparser access feed as remote and is the HTTP status ok
        if "status" not in parsed_rss or parsed_rss.status >= 400:
            raise FeedNotFoundError("Could not connect or find RSS feed")
        # Checks does parsed_feed object contain at least one main element of feed
        if "title" not in parsed_rss.feed and "link" not in parsed_rss and len(parsed_rss.entries) < 0:
            raise IncorrectRSSError("URL is not a correct RSS feed")

        logging.info("Feed successfully received")
        self.title = parsed_rss.feed.get("title") or parsed_rss.feed.get("link")

        if self.limit < 1 or self.limit > len(parsed_rss.entries):
            limit = len(parsed_rss.entries)
            logging.info("Parsing items without limit")
        else:
            limit = self.limit
            logging.info(f"Items limit is {limit}")
        self.items = []
        for i, entry in enumerate(parsed_rss.entries[:limit]):
            logging.info(f"Parsing item {(i+1)}")
            item = self._parse_remote_item(entry)
            if item is not None:
                self.items.append(item)
            else:
                logging.info("Skipping invalid item")

    def _parse_remote_item(self, entry):
        item = dict()
        if "published_parsed" not in entry:
            return None
        item["date"] = entry.published_parsed

        if "title" in entry:
            item["title"] = html.unescape(entry.title)
        else:
            item["title"] = None

        item["link"] = entry.get("link")

        if len(entry.enclosures) > 0:
            item["enclosure"] = entry.enclosures[0]
        else:
            item["enclosure"] = None

        item["description_parsed"] = None
        if "description" in entry:
            item["description"] = entry.description
            if self._is_html(entry.description_detail.type):
                item["description_parsed"] = html_to_text.parse(item["description"], skip_link=item.get("link"))
                logging.info("Item description is html and therefore converted to plain text")
        else:
            item["description"] = None
        return item

    def _load_cache(self):
        logging.info("Loading feed from cache")
        limit = -1
        if self.limit > 0:
            limit = self.limit
        db_feed = self.db.get_feed(self.link, self.date, limit)
        if db_feed is not None:
            logging.info("Feed successfully loaded")
            self.title = db_feed["title"]
            self.items = db_feed["items"]
        else:
            logging.warning("Feed with the specified link is not found in cache")

    def _save_to_cache(self):
        if self.db is not None:
            self.db.store_feed(self.link, self.title, self.items)
            logging.info("Feed saved to cache")

    def render_text(self):
        logging.info("Generating plain text representation of feed")

        s = []

        title = self.title or "no title"
        s.append(title)
        s.append("\n")
        if len(self.items) == 0:
            s.append("\nno items to show\n")
        else:
            for item in self.items:
                s.append("\n\n")

                item_title = item["title"] or "no title"
                s.append("Title: " + item_title + "\n")

                item_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", item["date"])
                s.append("Date: " + item_date + "\n")

                item_link = item["link"] or "no link"
                s.append("Link: " + item_link + "\n")

                s.append("\n")
                if item["enclosure"] is not None:
                    s.append("Enclosure: " + item["enclosure"]+"\n")
                    s.append("\n")

                s.append("Description: ")
                description = item["description_parsed"] or item["description"] or "no description"
                s.append(description)

        s = "".join(s)
        return s

    def render_json(self):
        logging.info("Generating json representation of feed")
        feed_dict = {"title": self.title, "items": self.items}
        s = json.dumps(feed_dict, indent="\t")
        return s

    @staticmethod
    def _try_fix_url(url):
        try:
            parsed_url = urllib.parse.urlsplit(url, "https")
        except ValueError:
            raise URLFormatError("Error in url format")
        else:
            result_url = urllib.parse.urlunsplit(parsed_url)
            return result_url if not result_url.endswith('/') else result_url[:-1]

    @staticmethod
    def _is_html(element_type):
        return element_type in ["text/html", "application/xhtml+xml"]
