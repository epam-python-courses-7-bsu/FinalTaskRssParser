from FinalTaskRssParser.final_task.rss_reader.data.rss_data_handler import RSSDataHandler
import re


class OutputHandler:
    def __init__(self, data: RSSDataHandler):
        self.feed = data.feed
        self.entries = data.get_entries()

    def to_readable(self):
        feed = "\nFeed: " + f'"{self.feed.title}"' + "\n\n"

        title, date, link, description, links = "", "", "", "", ""

        for element in self.entries:
            title = "Title: " + f"\"{element.title}\"" + '\n'
            date = "Date: " + f"{element.pub_date}" + '\n'
            link = "Link: " + f"{element.link}" + "\n" * 2
            description = f"{element.description}" + "\n" * 2

            links = list()
            for i, image in enumerate(element.image_links):
                if i != 0:
                    links.append(f"({i + 1}) >>> {image.get('href')} (image)")
                else:
                    links.append(f"({i + 1}) >>> {element.link} (link)")

            if links:
                links = "Links:\n" + ",\n".join(links)
            else:
                links = ""

            yield feed + title + date + link + description + links

        # return feed + title + date + link + description + links
