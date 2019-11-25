import logging as log
import requests as r
import check
import os
import datetime
import sys

from fpdf import FPDF
from dominate import document
from dominate.tags import div, h2, img, p

import printers

now = datetime.datetime.now


def create_html(items: list) -> document:
    """
        convert article data in html format
    """
    html_document = document(title='Dominate your HTML')
    log.info('Start make html format')
    for item in items:
        item = printers.prepare_one_item(item)
        with html_document:
            with div():
                h2("Title: " + item['Title:'])
                p("Link: " + item['Link: '])
                img(src=item['Media content:\n'])
                p("Description: " + item['Description: '])
                p("Date: " + item['Date:'])
    return html_document


def write_to_file(items: list) -> None:
    result = create_html(items)
    data = now().strftime("%d-%m-%Y")
    time = now().strftime("%X")
    name_of_html = str(data) + '_' + time
    with open("{}".format(name_of_html), "w") as f:
        f.write(str(result))
        log.info("Successful converting into html")


def create_pdf(items: list) -> None:
    log.info("Start creating pdf")
    date = now().strftime("%d-%m-%Y")
    time = now().strftime("%X")
    pdf = FPDF()
    element = str
    img_path = str
    try:
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 10)
    except RuntimeError:
        log.info("There isn't DejaVuSans.ttf in your rep")
        print("Something go wrong, check DejaVuSans.ttf in your rep ")
        sys.exit()
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
        pdf.write(8, "Date: " + str(item["Date:"]))
        pdf.ln(10)
        img_url = str(item['Media content:\n'])
        url_list = img_url.split("\n")

        # There's a difficult moment, cause 'fpdf' lib can't
        # get images from the Internet
        # So we should use temporary files

        if check.internet_on() and img_url != '':
            log.info("There is connection")
            try:
                for element in url_list:
                    # Try to understand format of image file
                    log.info("Try to understand format of image file")
                    if element.endswith(".png") or element.endswith(".jpg"):
                        image = r.get(element)
                        try:
                            img_path = str(len(element)) + \
                                       str(img_url[-4:])
                            with open(img_path, 'wb') as file:
                                file.write(image.content)
                                pdf.image(img_path, w=70, h=50)
                                pdf.ln(10)
                        # Some files have .jpg format, but have .jpeg ends
                        except RuntimeError:
                            log.info("Some files have .jpg format, but have .jpeg ends")
                            os.remove(img_path)
                            img_path = str(len(element)) + '_' + '.jpeg'
                            with open(img_path, 'wb') as file:
                                file.write(image.content)
                                pdf.image(img_path, w=70, h=50)
                                pdf.ln(10)
                    # We can't work with .gif, but we can show link of image
                    elif element.endswith(".gif"):
                        log.info("We can't work with .gif, but we can show link of image")
                        pdf.write(8, "I can't display images,"
                                     " but there's your links")
                        pdf.write(8, element)
                    # Some sites have duplicated links with double addresses,
                    # so we try to parse
                    else:
                        index_new_element = element.rfind('http')
                        new_element = element[index_new_element:]
                        image = r.get(new_element)
                        # They may have a format
                        if new_element.endswith(".jpg"):
                            img_path = str(len(new_element)) + \
                                       str(img_url[-4:])
                        # They may not have a format
                        else:
                            img_path = str(len(new_element)) + \
                                       '.jpg'
                        with open(img_path, 'wb') as file:
                            file.write(image.content)
                            pdf.image(img_path, w=70, h=50)
                            pdf.ln(10)
                    os.remove(img_path)
            # There are times when we can't insert pictures
            except (RuntimeError, ConnectionError):
                os.remove(img_path)
                pdf.write(8, "I can't display this image, "
                             "but there's your link")
                pdf.ln(10)
                pdf.write(8, str(element))
        # Cases where we don't have the Internet
        else:
            log.info("There isn't connection")
            pdf.write(8, str(item['Media content:\n']))
        pdf.ln(15)
        pdf.write(8, "Description: " + str(item['Description: ']))
        pdf.ln(10)
        pdf.write(8, "===End, news!===")
        pdf.ln(10)
    name_of_pdf = date + '_' + time + '.pdf'
    pdf.output(name_of_pdf, "F")
