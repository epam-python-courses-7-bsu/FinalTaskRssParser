"""  Module of functions for converting and saving news to pdf and html files.

     Functions:
     create_and_fill_pdf_file(news_collection, com_line_args, logger) -> None
     add_news_to_pdf_file(news, pdf, com_line_args, logger) -> None
     add_image(num, link, pdf, logger) -> None
     add_news_to_html_file(news, html_file, com_line_args, logger) -> None
     add_news_to_html_file(news, html_file, com_line_args, logger) -> html_file """

import os
import urllib.request
import urllib.error
from dominate.tags import *
from fpdf import FPDF, set_global
from validation_functions import check_path_to_directory
from exceptions import FilePathError


def create_and_fill_pdf_file(news_collection, com_line_args, logger):
    """ Function for creating and filling in the pdf file with news.  """
    path_to_directory = com_line_args.to_pdf

    check_path_to_directory(path_to_directory, logger)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(5, 13.5, 5)
    pdf.add_page()

    pdf.set_font('Arial', size=16)
    pdf.set_text_color(255, 0, 0)
    if com_line_args.date:
        pdf.cell(200, 10, txt="RSS news from the local storage", ln=1, align="C")
    else:
        pdf.cell(200, 10, txt="RSS news from the internet", ln=1, align="C")

    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    for news in news_collection:
        add_news_to_pdf_file(news, pdf, com_line_args, logger)
    logger.info("Creating pdf file with news.")
    path_to_pdf_file = os.path.join(path_to_directory, "rss_news.pdf")
    pdf.output(path_to_pdf_file, 'F')
    logger.info("PDF file is created.")


def add_news_to_pdf_file(news, pdf, com_line_args, logger):
    """ Function that add news to pdf file. """
    pdf.set_font('Arial', size=12)
    pdf.set_text_color(0, 255, 0)
    pdf.ln(10)
    pdf.multi_cell(0, 10, align="C", txt="News")
    pdf.set_text_color(0, 0, 255)
    pdf.write(10, "Feed title: ")
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt=f" {news.feed_title}")
    pdf.set_text_color(0, 0, 255)
    pdf.write(10, "News title: ")
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt=f"{news.title}")
    pdf.set_text_color(0, 0, 255)
    pdf.write(10, "News publication date: ")
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt=f"{news.date}")
    pdf.set_text_color(0, 0, 255)
    pdf.write(10, "Summary: ")
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt=f"{news.summary}")
    pdf.set_text_color(0, 0, 255)
    pdf.write(10, "News link: ")
    pdf.set_text_color(0, 0, 0)

    pdf.multi_cell(0, 10, txt=f"{news.link}")

    if news.image_links:
        if com_line_args.date:
            pdf.set_text_color(0, 0, 255)
            pdf.write(10, "Images links: ")
            pdf.set_text_color(0, 0, 0)
            for num, image_link in enumerate(news.image_links):
                pdf.write(10, f"[{num + 1}]: {image_link}" + '\n')
        else:
            pdf.set_text_color(0, 0, 255)
            pdf.write(10, "Images to summary: ")
            pdf.set_text_color(0, 0, 0)
            for num, img_link in enumerate(news.image_links):
                add_image(num + 1, img_link, pdf, logger)


def add_image(num, image_link, pdf, logger):
    """ Function for getting image from image url and adding it to pdf file. """
    logger.info(f"Download image from {image_link}.")

    (filename, headers) = urllib.request.urlretrieve(image_link)
    image_format = headers['content-type'].replace('image/', '')

    if image_format not in ('jpeg', 'jpg', 'png'):
        logger.info(f"Image from {image_link} is not in an appropriate format.")
        pdf.write(10, f"[{num}]: {image_link}" + '\n')
    else:
        pdf.image(filename, x=50, y=pdf.get_y(), h=30, type=image_format, link=image_link)
        pdf.ln(50)
        os.remove(filename)


def create_and_fill_html_file(news_collection, com_line_args, logger):
    """ Function for creating and filling in the html file with news.  """
    path_to_directory = com_line_args.to_html

    check_path_to_directory(path_to_directory, logger)

    html_file = html(title="RSS news")
    html_file.add(head(meta(charset='utf-8')))

    for news in news_collection:
        add_news_to_html_file(news, html_file, com_line_args)

    path = os.path.join(path_to_directory, "rss_news.html")
    try:
        logger.info("Creating html file with news.")
        with open(path, 'w', encoding='utf-8') as rss_html:
            rss_html.write(str(html_file))
        logger.info("HTML file is created.")
    except FileNotFoundError:
        logger.error("No html file directory.")
        raise FilePathError("No html file directory. Please, checked path.")


def add_news_to_html_file(news, html_file, com_line_args):
    """ Function that add news to html file. """
    with html_file:
        h1(news.title)
        p(b("Feed title: "), news.feed_title)
        p(b("Publication date: "), news.date)
        p(b("Summary: "), news.summary)
        p(a("Link for this news.", href=news.link))
        with p():
            if news.image_links:
                if com_line_args.date:
                    b("Images links: ")
                    for image_link in news.image_links:
                        a("Link to image", href=image_link)
                else:
                    b("Images to summary: ")
                    for img_link in news.image_links:
                        img(src=img_link)
        br()
        br()
    return html_file
