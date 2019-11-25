from dataclasses import dataclass
import datetime
import logging

MODULE_LOGGER = logging.getLogger("rss_reader.News")


@dataclass
class News:
    feed: str
    title: str
    date: datetime.datetime
    link: str
    info_about_image: str
    briefly_about_news: str
    links_from_news: list

    def get_json(self):
        """
            returns news in json format
        """
        logger = logging.getLogger("rss_reader.News.get_json")
        logger.info("return news in json format")
        data = {
            "Feed": self.feed,
            "Title": self.title,
            "Date": str(self.date),
            "Link": self.link,
            "Info about image": self.info_about_image,
            "Briefly about news": self.briefly_about_news,
            "Links": self.links_from_news

        }
        return data

    def __str__(self):
        """
           Return a string representation of the news for print in stdout.
        """
        logger = logging.getLogger("rss_reader.News.__str__")
        logger.info("return str")
        links = ""
        for index, link in enumerate(self.links_from_news or []):
            if link:
                links += "[" + str(index) + "] " + link + "\n"

        return f"Feed: {self.feed}\n" \
               f"Title: {self.title} \n" \
               f"Date: {self.date} \n" \
               f"Link: {self.link}\n" \
               f"Info about image: {self.info_about_image}\n" \
               f"Briefly about news: {self.briefly_about_news}\n" \
               f"Links: \n{links}"
