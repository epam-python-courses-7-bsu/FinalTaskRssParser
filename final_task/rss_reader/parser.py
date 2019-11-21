import logging
from bs4 import BeautifulSoup
from news_articles import NewsArticle


def xml_parser(response, limit):
    """get response and parse it to get NewsArticle object"""
    logging.info('Starting to parse XML data')
    soup = BeautifulSoup(response, 'xml')
    news_outlett_name = soup.title.text

    news_soup = soup('item')
    news_articles = []
    for article in news_soup:
        if len(news_articles) == limit:
            break
        pub_date = article.pubDate.text
        news_link = article.link.text

        # make the soup again because codes such as &#39; didn't decode at first step
        news_title = BeautifulSoup(article.title.text, 'lxml').text
        if article.find('description'):
            # make soup again because we couldn't go deeper down the tree(couldn't recognize some tags)
            description_soup = BeautifulSoup(article.description.text, 'lxml')
            news_description = description_soup.text
            if description_soup.find('img'):
                img_alt = description_soup.img.get('alt')
                img_src = description_soup.img.get('src')
            else:
                img_alt = ''
                img_src = ''
            news_articles.append(NewsArticle(news_outlett_name, news_title, pub_date, news_link,
                                             news_description, img_alt, img_src))
        else:
            news_description = ''
            news_articles.append(NewsArticle(news_outlett_name, news_title, pub_date, news_link,
                                             news_description))
    logging.info('Parsing is finished')
    return news_articles
