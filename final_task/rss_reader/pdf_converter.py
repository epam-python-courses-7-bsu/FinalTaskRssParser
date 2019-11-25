"""Module converts articles to pdf file"""
import logging
import os
import urllib.request
import datetime
from typing import Optional

from fpdf import FPDF, set_global

import custom_error
from argparse_handler import check_the_connection

directory_to_module = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.join(directory_to_module, 'font')


def convert_to_pdf(articles_list: list, path: str, rss_url: Optional[str]) -> None:
    """Converts articles to pdf format"""
    try:
        set_global("FPDF_CACHE_MODE", 1)
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(10, 10, 10)
        pdf.add_page()
        try:
            pdf.add_font('dejavu', '', os.path.join(FONT_PATH, 'dejavusans.ttf'), uni=True)
        except RuntimeError:
            raise custom_error.FontNotFoundError("Can't find dejavusans.ttf font. Can't convert to PDF.")
        pdf.set_font('dejavu')

        connection = check_the_connection('https://www.google.com/')[0]

        if connection:
            logging.info("Converting to pdf with images")
        else:
            logging.info("Converting to pdf without images")

        for index, article in enumerate(articles_list, 1):
            pdf.set_font_size(20)
            pdf.cell(w=0, txt=f'Article #{index}')
            pdf.ln(10)

            pdf.set_font_size(10)
            pdf.multi_cell(w=0, h=5, txt=f'Feed: {article.feed}')
            pdf.ln(5)
            pdf.multi_cell(w=0, h=5, txt=f'Title: {article.title}')
            pdf.ln(5)
            pdf.cell(w=0, txt=f'Date: {article.date}')
            pdf.ln(5)
            pdf.multi_cell(w=0, h=5, txt=f'Link: {article.link}')
            pdf.ln(5)
            pdf.multi_cell(w=0, h=5, txt=f'{article.summary}')
            pdf.ln(5)

            pdf.cell(w=0, txt=f'Links:')
            pdf.ln(5)
            if connection:
                for number, link in enumerate(article.links, 1):

                    if link[1] == 'image':
                        try:
                            filename, headers = urllib.request.urlretrieve(link[0])
                            image_type = headers['content-type'].replace('image/', '')

                            if image_type in ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']:
                                pdf.cell(w=0, txt=f'[{number}]: ')
                                pdf.image(filename, x=20, y=pdf.get_y(), h=20, type=image_type)
                                pdf.ln(25)
                                os.remove(filename)
                            else:
                                pdf.multi_cell(w=0, h=5, txt=f'[{number}]: {link[0]}')
                                pdf.ln(5)
                        except (ConnectionError, urllib.request.ContentTooShortError):
                            pdf.multi_cell(w=0, h=5, txt=f'[{number}]: {link[0]}')
                            pdf.ln(5)
                    else:
                        pdf.multi_cell(w=0, h=5, txt=f'[{number}]: {link[0]}')
                        pdf.ln(5)

            else:
                for number, link in enumerate(article.links, 1):
                    pdf.multi_cell(w=0, h=5, txt=f'[{number}]: {link[0]}')
                    pdf.ln(5)

            pdf.ln(20)

        today = datetime.date.today().strftime("%B %d, %Y")
        if rss_url:
            filename = f'{today} {urllib.request.urlparse(rss_url).netloc}.pdf'
        else:
            filename = f'{today}.pdf'

        full_name = os.path.join(path, filename)
        pdf.output(full_name, 'F')
    except PermissionError:
        print('Please, close pdf file before converting or you need to run program as system administrator, '
              'to save files in that location')
    except custom_error.FontNotFoundError as error:
        print(error.message)
