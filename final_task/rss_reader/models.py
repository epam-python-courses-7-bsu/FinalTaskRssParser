""" Data models module """
from dataclasses import dataclass, field


@dataclass
class NewsEntry:
    """ Class representing a news article(entry).

        Methods:
        print_entry(self) - print entry in stdout """

    feed_title: str = ""
    feed_language: str = ""

    title: str = ""
    summary: str = ""
    date: str = ""
    link: str = ""
    source: str = ""
    image_links: list = field(default_factory=list)

    def print_entry(self):
        print("-------------------------------------------------------------",
              "Feed title: " + self.feed_title + '\n',
              "Feed language: " + self.feed_language + '\n' + '\n',
              "News title: " + self.title + '\n',
              "Summary: " + self.summary + '\n',
              "Publication date: " + self.date + '\n',
              "Source: " + self.source + '\n',
              "Link: " + self.link + '\n',
              sep='\n')

        if self.image_links:
            print("Images links: ")
            for num, img_link in enumerate(self.image_links):
                if img_link:
                    print(f"[{num+1}] {img_link}")
