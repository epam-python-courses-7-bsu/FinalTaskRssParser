"""Module for epub and html convertation"""

from functions.check_func import check_internet_connection
from classes.exceptions import InternetConnectionError, DirectoryError
from functions.print_func import check_limit_argument

from ebooklib import epub
import os
import dominate
import dominate.tags as tag


def create_epub_object():
    book = epub.EpubBook()
    book.set_identifier('486464534')
    book.set_title('News book')
    book.set_language('en')
    book.add_author('Anton Zimahorau')
    return book


def create_epub(command_line_args, news_collection, logger):
    """Creates epub book from news collection"""
    news_collection = check_limit_argument(command_line_args, news_collection, logger)

    book = create_epub_object()
    book.spine = ['nav']
    # Internet connection checking
    try:
        internet = check_internet_connection(logger)
    except InternetConnectionError:
        internet = False


    logger.info("Creating epub News book...")
    for num, news in enumerate(news_collection):
        logger.info("Create chapter {}".format(num+1))

        chapter = epub.EpubHtml(title=news.title, file_name=str(num))

        doc_html = dominate.document(title='RSS News')
        doc_html = create_html_news_entry(news, doc_html, internet)
        content = str(doc_html)

        chapter.set_content(content)
        book.add_item(chapter)
        book.spine.append(chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    dir = os.path.join(command_line_args.to_epub, 'News.epub')
    try:
        with open(dir, 'w') as h:
            h.write("r")
        epub.write_epub(dir, book)
        logger.info("Epub book is created")
    except FileNotFoundError:
        raise DirectoryError("No such directory")



def create_html(command_line_args, news_collection, logger):
    """Creates html file"""
    news_collection = check_limit_argument(command_line_args, news_collection, logger)

    logger.info("Creating html file...")
    doc_html = dominate.document(title='RSS News')
    with doc_html:
        tag.h1("RSS News")

    # Internet connection checking
    try:
        internet = check_internet_connection(logger)
    except InternetConnectionError:
        internet = False

    for num, news in enumerate(news_collection):
        logger.info("Add entry {}".format(num + 1))
        doc_html = create_html_news_entry(news, doc_html, internet)

    dir = os.path.join(command_line_args.to_html, 'News.html')
    try:
        with open(dir, 'w') as h:
            h.write(str(doc_html))
        logger.info("HTML file is created")
    except FileNotFoundError:
        raise DirectoryError("No such directory")



def create_html_news_entry(news, doc_html, internet):
    """Create html for news entry"""
    images_links = news.links[1]
    all_links = news.create_list_of_links()

    with doc_html:
        tag.h1(news.title)
        with tag.p(news.date):
            tag.br()
            tag.a("Link to this article", href=news.link)
        if internet:
            for link in images_links:
                tag.img(src=link)
        tag.p(news.text)
        for num, link in enumerate(all_links):
            tag.a("Link №{}".format(num + 1), href=link)
            tag.br()
    return doc_html
