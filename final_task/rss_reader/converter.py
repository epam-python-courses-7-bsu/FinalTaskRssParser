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


def get_path(path, expansion_file):
    logger = logging.getLogger("rss_reader.converter.get_path")
    logger.info("return correct path")
    if not fnmatch.fnmatch(path, '*%s' % expansion_file):
        raise FileNotFoundError("Invalid expansion ")
    if not os.path.isdir(path[:path.rfind("/")]):
        raise FileNotFoundError("File or directory not found")
    result = path
    return result


def conversion_of_news_in_html(path, list_of_news: list):
    logger = logging.getLogger("rss_reader.converter.conversion_of_news_in_html")
    logger.info("conversion of news in html")
    correct_path = get_path(path, ".html")
    with open(correct_path, 'w') as file:
        for news in list_of_news:
            doc = dominate.document(title='RSS READER')
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

            file.write(doc.render())
        print("news successfully saved to file  ", path)


def get_img(name, reference):
    logger = logging.getLogger("rss_reader.converter.get_img")
    logger.info("return img")
    is_picture = False
    try:
        response = requests.get(reference)
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 100))
        img = img.convert('RGB')
        img.save(name, 'JPEG')
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


def text_separator(text: str, break_long_words) -> str:
    logger = logging.getLogger("rss_reader.converter.text_separator")
    logger.info("return text")
    format_text = textwrap.fill(text, width=50, break_long_words=break_long_words)
    ls = format_text.split('\n')
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


def print_line_in_pdf(canvas, line, x, y):
    logger = logging.getLogger("rss_reader.converter.print_line_in_pdf")
    logger.info("print line in pdf")
    if y < 25:
        canvas.showPage()
        canvas.setFont('FreeSans', 19)
        y = 900
    y -= 25
    canvas.drawString(x, y, line)
    return y - 25


def conversion_of_news_in_pdf(path, list_of_news):
    logger = logging.getLogger("rss_reader.converter.conversion_of_news_in_pdf")
    logger.info("conversion_of_news_in_pdf")
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
    print("news successfully saved to file  ", path)
