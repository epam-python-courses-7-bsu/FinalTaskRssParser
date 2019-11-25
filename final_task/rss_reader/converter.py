import fnmatch
import logging
import os
import textwrap
from io import BytesIO

import dominate
import requests
from PIL import Image
from dominate import tags
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

MODULE_LOGGER = logging.getLogger("rss_reader.converter")


def get_path(path: str, expansion_file: str) -> str:
    """
    Checks the correctness of the entered path
    if received path to directory check her on exist
    if directory exist add News and expansion file
    if received path to file check his on exist and check correctness expansion file
    :param path:
    :param expansion_file:
    :return:
    """
    logger = logging.getLogger("rss_reader.converter.get_path")
    logger.info("check path")
    if os.path.isdir(path):
        logger.info("path specified to directory")
        result = path + '/News' + expansion_file
    else:
        if not fnmatch.fnmatch(path, '*%s' % expansion_file):
            logger.error("Invalid expansion ")
            raise FileNotFoundError(f"Invalid expansion {path}")
        if not os.path.isdir(path[:path.rfind("/") + 1]):
            logger.error("File or directory not found")
            raise FileNotFoundError(f"File or directory not found {path}")
        result = path
    return result


def get_html(list_of_news: list):
    """
    Forms html content
    :param list_of_news:
    :return:
    """
    logger = logging.getLogger("rss_reader.converter.get_html")
    logger.info("getting html content")
    doc = dominate.document(title='RSS READER')
    for news in list_of_news:
        with doc.head:
            tags.link(rel='stylesheet', href='style.css')
            tags.script(type='text/javascript', src='script.js')
            tags.style("""\
                     body {
                         background-color: #F9F8F1;
                         color: #2C232A;
                         font-family: sans-serif;
                         font-size: 2.6em;
                         margin: 3em 1em;
                     }

                 """)

        with doc:
            with tags.div(id='header'):
                tags.p("Feed: ", news.feed)
                tags.p("Title: ", news.title)
                tags.p("Date ", str(news.date))
                tags.p("Link: ", tags.a(news.link.title(), href=news.link, target="_blank"))
                tags.p("Info about image: ", news.info_about_image)
                tags.p("Briefly about news: ", news.briefly_about_news)
                tags.p("Links: ", )
                for reference in news.links_from_news:
                    if reference:
                        tags.li(tags.a(reference.title(), href=reference, target="_blank"))
                if news.links_from_news[1]:
                    tags.a(tags.img(
                        src=news.links_from_news[1],
                        width="200", height="200", alt=news.info_about_image),
                        href=news.links_from_news[1], target="_blank")
    logger.info("html content received")
    return doc


def conversion_of_news_in_html(path, list_of_news):
    logger = logging.getLogger("rss_reader.converter.conversion_of_news_in_html")
    logger.info("conversion of news in html")
    correct_path = get_path(path, ".html")
    html_content = get_html(list_of_news)
    save_html(correct_path, html_content)
    logger.info("conversion of news in html successful completed")


def save_html(path, html_content):
    """
    Save news in file
    :param path:
    :param html_content:
    :return:
    """
    logger = logging.getLogger("rss_reader.converter.save_html")
    try:
        with open(path, 'w') as file:
            file.write(html_content.render())
        print("news successfully saved to file ", path)
        logger.info("news successfully saved to file  ")
    except MemoryError:
        logger.error("not enough memory to save html file")
        print("You do not have enough memory to save html file")


def get_img(image_name, reference):
    """
    Download image in file
    :param image_name:
    :param reference:
    :return: True if image successfully downloaded
    """
    logger = logging.getLogger("rss_reader.converter.get_img")
    logger.info("return img")
    is_picture = False
    try:
        response = requests.get(reference)
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 100))
        img = img.convert('RGB')
        img.save(image_name, 'JPEG')
        is_picture = True
    except requests.exceptions.ConnectionError:
        logger = logging.getLogger("rss_reader.converter.get_img")
        logger.error("You do not have an internet connection\n"
                     "your news will be saved in pdf without pictures")
    except requests.exceptions.MissingSchema:
        logger = logging.getLogger("rss_reader.converter.get_img")
        logger.error("Invalid url picture \n")
    except OSError:
        logger = logging.getLogger("rss_reader.converter.get_img")
        logger.error("cannot identify image\n")
    return is_picture


def text_separator(text: str, break_long_words: bool) -> list:
    """
    Breaks text into lines of 50 characters
    :param text:
    :param break_long_words:
    :return:
    """
    logger = logging.getLogger("rss_reader.converter.text_separator")
    format_text = textwrap.fill(text, width=50, break_long_words=break_long_words)
    ls = format_text.split('\n')
    logger.info("text successfully broken")
    return ls


def print_text_in_pdf(canvas, text, x, y):
    logger = logging.getLogger("rss_reader.converter.print_list_in_pdf")
    logger.info("print list in pdf")
    ls = text_separator(text, False)
    for lines in ls:
        if y < 45:
            canvas.showPage()
            canvas.setFont('FreeSans', 19)
            y = 800
        y -= 25
        canvas.drawString(x, y, lines)
    return y - 25


def conversion_of_news_in_pdf(path, list_of_news):
    logger = logging.getLogger("rss_reader.converter.conversion_of_news_in_pdf")
    correct_path = get_path(path, ".pdf")
    canvas = Canvas(correct_path, pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    canvas.setFont('FreeSans', 19)
    canvas.setTitle("RSS READER")
    x = 10
    y = 800
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    name_buffer_picture_file = "tmp1"
    for index, news in enumerate(list_of_news):
        name_buffer_picture_file = name_buffer_picture_file[:-1] + str(index)
        canvas.setFont('FreeSans', 19)
        if get_img(name_buffer_picture_file + '.jpg', news.links_from_news[1]):
            y -= 170
            if y < 45:
                canvas.showPage()
                canvas.setFont('FreeSans', 19)
                y = 680
            canvas.drawImage(name_buffer_picture_file + ".jpg", x, y, 150, 150)
            os.remove(name_buffer_picture_file + '.jpg')
            y -= 40
        y = print_text_in_pdf(canvas, news.feed, x, y)
        y = print_text_in_pdf(canvas, news.title, x, y)
        y = print_text_in_pdf(canvas, str(news.date), x, y)
        y = print_text_in_pdf(canvas, news.link, x, y)
        y = print_text_in_pdf(canvas, news.info_about_image, x, y)
        y = print_text_in_pdf(canvas, news.briefly_about_news, x, y)
        if y < 45:
            canvas.showPage()
            y = 800
    logger.info("save news in pdf")
    canvas.save()
    print("news successfully saved to file  ", correct_path)
