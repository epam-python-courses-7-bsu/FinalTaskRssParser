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

                list_links = []
                for group1 in re.finditer(LINKS_TEMPLATE, xml_news_item.text):
                    list_links.append(group1.group(1))
                    parser_dictionary['links'] = list_links

        dict_article_list.append(parser_dictionary)

        if limit == counter + 1:
            return dict_article_list
    return dict_article_list

def dicts_to_articles(dict_list):
    """This function receive list of dictionaries and convert it to list of articles """
    article_list = []
    for item in dict_list:
        article_list.append(MyArticle(item))
    return article_list

@dataclass
class MyArticle:
    """This is news class, which receives dictionary and have title, date, link, article and links keys fields"""
    def __init__(self, article_dict):
        self.title = article_dict['title']
        self.date = article_dict['date']
        self.link = article_dict['link']
        self.article = article_dict['article']
        self.links_list = article_dict['links']

    def __str__(self):
        result_string_article = '\n'
        result_string_article += "Title: {}\nDate: {}\nLink: {}\n\n{}\n\n".format(self.title, self.date, self.link,
                                                                                  self.article)
        for link_idx, link in enumerate(self.links_list):
            result_string_article += "[{}]: {}\n".format(link_idx + 1, link)
        result_string_article += '\n'
        return result_string_article
