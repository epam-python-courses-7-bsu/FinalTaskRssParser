import re
import html2text
from dataclasses import dataclass


LINKS_TEMPLATE = '\"((http|https)://(\w|.)+?)\"'


def xml_arguments_for_class(xml_string, limit):
    """This function receive the xml and limit of articles and returns list of dictionaries"""
    dict_article_list = []
    text = html2text.HTML2Text()
    text.ignore_images = True
    text.ignore_links = True
    text.ignore_emphasis = True
    for counter, xml_news in enumerate(xml_string.iter('item')):
        parser_dictionary = {}
        for xml_news_item in xml_news:
            # Here we create the article in the form of a dictionary
            if xml_news_item.tag == 'title':
                parser_dictionary['title'] = text.handle(xml_news_item.text).replace('\n', "")

            if xml_news_item.tag == 'pubDate':
                parser_dictionary['date'] = xml_news_item.text

            if xml_news_item.tag == 'link':
                parser_dictionary['link'] = xml_news_item.text

            if xml_news_item.tag == 'description':
                parser_dictionary['article'] = text.handle(xml_news_item.text).replace('\n', '')
                parser_dictionary['links'] = xml_news_item.text.replace('\n', '')

        dict_article_list.append(parser_dictionary)

        if limit == counter + 1:
            return dict_article_list
    return dict_article_list

def dicts_to_articles(dict_list):
    """This function receive list of dictionaries and convert it to list of articles """
    article_list = []
    for item in dict_list:
        article_list.append(Article(**item))
    return article_list

def html_text_to_list_links(html_links):
    html_links = html_links.replace("\'", "\"")
    list_links = []
    for group1 in re.finditer(LINKS_TEMPLATE, html_links):
        list_links.append(group1.group(1))
    return list_links

@dataclass
class Article:
    """This is news class, which receives dictionary and have title, date, link, article and links keys fields"""
    title: str
    date: str
    link: str
    article: str
    links :str

    def __post_init__(self):
        self.links = html_text_to_list_links(self.links)

    def __str__(self):
        result_string_article = "\nTitle: %s\nDate: %s\nLink: %s\n\n%s\n\n" % (self.title, self.date, self.link,
                                                                                  self.article)
        for link_idx, link in enumerate(self.links):
            result_string_article += "[%d]: %s\n" % (link_idx + 1, link)
        result_string_article += '\n'
        return result_string_article

    def __eq__(self, other):
        if self.article == other.article and self.title == other.title and self.link == other.link and \
                self.date == other.date:
            return True
        return False
