from dataclasses import dataclass
import datetime
import logging

module_logger = logging.getLogger("rss_reader.scripts.News")


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
        logger = logging.getLogger("rss_reader.scripts.News.get_json")
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
        logger = logging.getLogger("rss_reader.scripts.News.__str__")
        logger.info("return str")
        links = ""
        for index, link in enumerate(self.links_from_news or []):
            links += "[" + str(index) + "] " + link + "\n"

        return "Feed: {feed}\n" \
               "Title: {title} \n" \
               "Date: {date} \n" \
               "Link: {link}\n" \
               "Info about image: {info_about_image}\n" \
               "Briefly about news: {briefly_about_news}\n" \
               "Links: \n{links}".format(feed=self.feed,
                                         title=self.title,
                                         date=self.date,
                                         link=self.link,
                                         info_about_image=self.info_about_image,
                                         briefly_about_news=self.briefly_about_news,
                                         links=links)
