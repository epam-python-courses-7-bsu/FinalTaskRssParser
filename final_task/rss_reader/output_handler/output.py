from data import RSSDataHandler
from json import dumps
import re


class OutputHandler:
    def __init__(self, data: RSSDataHandler, is_colored=False):
        self.data = data
        self.feed = data.feed
        self.is_colored = is_colored
        self.entries = data.get_entries()

    def format_news(self):
        feed = "\nFeed: " + f'"{self.feed.title}"' + "\n\n"

        # title, date, link, description, links = "", "", "", "", ""

        for element in self.entries:
            title = "Title: " + f"\"{element.title}\"" + '\n'
            date = "Date: " + f"{element.pub_date}" + '\n'
            link = "Link: " + f"{element.link}" + "\n" * 2
            description = f"{element.description}" + "\n" * 2

            links = list()
            for index, image in enumerate(element.image_links):
                if index != 0:
                    links.append(f"({index + 1}) >>> {image.get('href')} (image)")
                else:
                    links.append(f"({index + 1}) >>> {element.link} (link)")

            if links:
                links = "Links:\n" + ",\n".join(links)
            else:
                links = ""

            formatted_news = feed + title + date + link + description + links

            if self.is_colored:
                yield self.colorize(formatted_news)
            else:
                yield formatted_news

    def format_to_json_string(self):
        return dumps(self.data.create_data_dict(), indent=2, ensure_ascii=False)

    def colorize(self, formatted_news):
        # colors: grey, red, green, yellow, blue, magenta, cyan, white
        # highlights:
        dict_of_news = self.data.create_data_dict()

        formatted_news = re.sub("\"" + dict_of_news['feed']['title'] + "\"",
                                '\033[92m' + "\"" + dict_of_news['feed']['title'] + "\"" + '\033[0m',
                                formatted_news)
        formatted_news = re.sub('Feed:', '\033[97m' + "Feed:" + '\033[0m', formatted_news)
        formatted_news = re.sub('Title:', '\033[93m' + "Title:" + '\033[0m', formatted_news)
        formatted_news = re.sub('Date:', '\033[95m' + "Date:" + '\033[0m', formatted_news)
        formatted_news = re.sub('Link:', '\033[96m' + "Link:" + '\033[0m', formatted_news)
        formatted_news = re.sub('Links:', '\033[32m' + "Links:" + '\033[0m', formatted_news)
        return formatted_news
