import feedparser
from dataclasses import dataclass, asdict
import html

from Log import log_decore


# convert from News class to json
@log_decore
def parse_to_json(news):
    return asdict(news)


# news kept
@dataclass
class News:
    news: str
    link: str
    title: str
    date: str
    links: []


class Handler:
    @log_decore
    # limit - count elements which user want see
    def __init__(self, url, limit):

        self.article = feedparser.parse(url)
        self.numb_news = 0
        self.parsers = []
        # standart value if user did not indicate limit we get all news
        if limit == -1:
            limit = len(self.article.entries)
        self.create_news(url, limit)
    @log_decore
    def create_news(self, url, limit):
        # for every news, which user will see we create object
        while self.numb_news < limit:
            tmp_img_link = self.get_img_links(self.get_news(self.numb_news))
            tmp_news = self.parse_html(self.get_news(self.numb_news))
            t = News(tmp_news, url, self.get_title(self.numb_news), self.get_date(self.numb_news), tmp_img_link)
            self.parsers.append(t)
            self.numb_news += 1

    @log_decore
    def get_news(self, index):
        try:
            return self.article.entries[index].summary
        except IndexError:
            pass

    @log_decore
    def get_title(self, index):

        return html.unescape(self.article.entries[index].title)

    @log_decore
    def get_date(self, index):
        return self.article.entries[index].published

    @log_decore
    def get_img_links(self, text):
        img_links = []
        index_start_find = 0
        while 1:
            start = text.find('src="', index_start_find, len(text))
            index_start_find = start + len('src="')
            end = text.find('"', index_start_find)
            if start == -1 or end == -1:
                break
            img_links.append(text[start + len('src="'):end])
        return img_links

    @log_decore
    def get_img_alt(self, text):
        img_alt = []
        index_start_find = 0
        while 1:
            start = text.find('alt="', index_start_find, len(text))
            index_start_find = start + len('alt="')
            end = text.find('"', index_start_find)
            if start == -1 or end == -1:
                break
            img_alt.append(text[start + len('alt="'):end])
        return img_alt

    @log_decore
    def parse_html(self, text):
        news = ""
        img_alt = self.get_img_alt(text)
        # add imgLinks to article
        for id, item in enumerate(img_alt):
            news += ("[img " + str(id)+" ")
            news += (item + "]")

        # clean the news from
        while text.count('<'):
            text = text[:text.find('<')] + text[text.find('>') + 1:]
        news += text
        news = html.unescape(news)
        return news

    @log_decore
    def get_all(self):
        # return all news which user want see
        return self.parsers
