"""Module for epub and html convertation"""

from ebooklib import epub
import os
import requests
import dominate
import dominate.tags as tag

from functions.check_func import check_internet_connection
from classes.exceptions import InternetConnectionError, DirectoryError
from functions.print_func import limit_news_collections


def set_internet_flag(logger):
    """If Internet connection, set flag to True, else False"""
    try:
        internet = check_internet_connection(logger)
    except InternetConnectionError:
        internet = False
    return internet


def create_html(command_line_args, news_collection, logger):
    """Creates html file"""
    news_collection = limit_news_collections(command_line_args, news_collection, logger)

    logger.info("Creating html file...")
    doc_html = dominate.document(title='RSS News')
    with doc_html.head:
        tag.meta(charset='utf-8')
    with doc_html:
        tag.h1("RSS News")
    # Internet connection checking
    internet = set_internet_flag(logger)

    for num, news in enumerate(news_collection):
        logger.info("Add html entry {}".format(num + 1))
        doc_html = create_html_news_entry(news, doc_html, internet)

    path_to_html = os.path.join(command_line_args.to_html, 'RSS News.html')
    try:
        with open(path_to_html, 'w') as html_obj:
            html_obj.write(str(doc_html))
        logger.info("HTML file is created")
    except FileNotFoundError:
        raise DirectoryError(f"There are no directory {command_line_args.to_html}")


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
        else:
            for link in images_links:
                tag.a("Image link", href=link)
        tag.p(news.text)
        for num, link in enumerate(all_links):
            tag.a("Link №{}".format(num + 1), href=link)
            tag.br()
    return doc_html


def create_epub_object():
    """Create EpubBook object"""
    book = epub.EpubBook()
    book.set_identifier('486464534')
    book.set_title('News book')
    book.set_language('en')
    book.add_author('Anton Zimahorau')

    # define css style
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
    }
    h2 {
         text-align: left;
         text-transform: uppercase;
         font-weight: 200;     
    }
    ol {
            list-style-type: none;
    }
    ol > li:first-child {
            margin-top: 0.3em;
    }
    nav[epub|type~='toc'] > ol > li > ol  {
        list-style-type:square;
    }
    nav[epub|type~='toc'] > ol > li > ol > li {
            margin-top: 0.3em;
    }
    '''

    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    book.spine = ['nav']
    return book


def create_epub(command_line_args, news_collection, logger):
    """Creates epub book from news collection"""
    news_collection = limit_news_collections(command_line_args, news_collection, logger)

    book = create_epub_object()

    # Internet connection checking
    internet = set_internet_flag(logger)

    logger.info("Creating epub News book...")
    image_number = 0
    for num, news in enumerate(news_collection):
        logger.info("Create epub book chapter {}".format(num+1))

        if internet:
            list_of_images_objects, image_number = create_image_objects(news, image_number)
            for img_obj in list_of_images_objects:
                book.add_item(img_obj)
        else:
            list_of_images_objects = []

        chapter = epub.EpubHtml(title=news.title, file_name=str(num), media_type="application/xhtml+xml")
        doc_html = dominate.document(title='RSS News')
        doc_html = create_html_news_entry_for_epub(news, doc_html, internet, list_of_images_objects)
        content = str(doc_html)

        chapter.set_content(content)
        book.add_item(chapter)
        book.spine.append(chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    path_to_ebook = os.path.join(command_line_args.to_epub, 'RSS News.epub')
    epub.write_epub(path_to_ebook, book, {})
    if os.path.exists(path_to_ebook):
        logger.info("Epub book is created")
    else:
        raise DirectoryError(f"There are no directory {command_line_args.to_epub}")


def create_html_news_entry_for_epub(news, doc_html, internet, list_of_image_objects):
    """Create html for epub news entry"""
    images_links = news.links[1]
    all_links = news.create_list_of_links()

    with doc_html:
        tag.h1(news.title)
        with tag.p(news.date):
            tag.br()
            tag.a("Link to this article", href=news.link)
        if internet:
            for image_object in list_of_image_objects:
                tag.img(src=image_object.file_name)
        else:
            for link in images_links:
                if link:
                    tag.a("Image link", href=link)
        tag.p(news.text)
        for num, link in enumerate(all_links):
            tag.a(f"Link №{num+1}", href=link)
            tag.br()
    return doc_html


def download_images(news):
    """Download images and return list of bytestrings images"""
    images_links = news.links[1]
    list_of_images = []


    for link in images_links:
        if link:
            responce = requests.get(link)
            if responce.status_code == 200:
                image = responce.content
                list_of_images.append(image)
    return list_of_images


def create_image_objects(news, image_number):
    """Return list of epubImage objects"""
    list_of_image_objects = []
    list_of_images = download_images(news)
    for image in list_of_images:
        img_obj = epub.EpubImage()
        img_obj.file_name = f"{image_number}.jpg"
        image_number += 1
        img_obj.media_type = "image/jpeg"
        img_obj.set_content(image)
        list_of_image_objects.append(img_obj)
    return list_of_image_objects, image_number
