import logging as log
import dominate
from fpdf import FPDF
from dominate import document
from dominate.tags import div, h2, img, p
import requests as r
import printers
import check
import os
import re
import random


def create_html(items: list) -> document:
    """convert article data in html format"""
    html_document = dominate.document(title='Dominate your HTML')
    log.info('Start make html format')
    for item in items:
        item = printers.prepare_one_item(item)
        with html_document:
            with div():
                h2("Title: " + item['Title:'])
                p("Link: " + item['Link: '])
                img(src=item['Media content:\n'])
                p("Description: " + item['Description:\n'])
    return html_document


def write_to_file(items: list) -> None:
    result = create_html(items)
    with open("html_file", "w", encoding="utf-8") as f:
        f.write(str(result))
        log.info("Successful converting into html")


def create_pdf(items: list) -> None:
    pdf = FPDF()
    try:
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 14)
    except RuntimeError:
        log.info("There isn't DejaVuSans.ttf in your rep")
    pdf.write(8, "RSS feed")
    pdf.ln(20)
    for item in items:
        item = printers.prepare_one_item(item)
        pdf.write(8, "===Wow! News!===")
        pdf.ln(10)
        pdf.write(8, "Title: " + str(item['Title:']))
        pdf.ln(10)
        pdf.write(8, "Link: " + str(item['Link: ']))
        pdf.ln(15)
        img_url = str(item['Media content:\n'])
        url_list = img_url.split("\n")
        if check.internet_on and img_url != '':
            for element in url_list:
                if element.endswith(".png") or element.endswith(".jpg"):
                    image = r.get(element)
                    img_path = str(len(element)) + str(random.randint(1, 128)) + str(img_url[-4:])
                    with open(img_path, 'wb') as file:
                        file.write(image.content)
                        pdf.image(img_path, w=70, h=50)
                elif element.endswith(".gif"):
                    pdf.write(8, "I can't display, but there's your link")
                    pdf.write(8, str(element))
                else:
                    index_new_element = element.rfind('http')
                    new_element = element[index_new_element:]
                    image = r.get(new_element)
                    img_path = str(len(new_element)) + str(random.randint(1, 128)) + '.jpg'
                    with open(img_path, 'wb') as file:
                        file.write(image.content)
                        pdf.image(img_path, w=70, h=50)
                os.remove(img_path)
        else:
            pdf.write(8, "Media content: " + str(item['Media content:\n']))
        pdf.ln(15)
        pdf.write(8, "Description: " + str(item['Description: ']))
        pdf.ln(10)
        pdf.write(8, "===End, news!===")
        pdf.ln(10)
    pdf.output("news.pdf", "F")
