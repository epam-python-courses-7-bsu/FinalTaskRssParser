#!/usr/bin/env python3.8

import os
import urllib.request

from fpdf import FPDF, set_global

from rss_exceptions import PATHError
from utils import create_path_to_file


CUR_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.join(CUR_DIRECTORY, 'fonts')


def convert_news_to_pdf(cmd_args, all_news, logger):
    """
    If the 'to-pdf' argument was passed - creates PDF file and push data in it.
    """
    if cmd_args.to_pdf:
        logger.info("Call function for creation PDF file")
        create_pdf_file(cmd_args, all_news, logger)


def create_pdf_file(cmd_args, all_news, logger):
    """
    Creates and fills in the PDF file with the required data
    """
    path_to_pdf = create_path_to_file(cmd_args.to_pdf, 'RSS_NEWS.pdf', logger)

    # --- normal cache mode ---
    set_global("FPDF_CACHE_MODE", 0)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(5, 10, 5)
    pdf.add_page()

    # use downloaded unicode font
    pdf.add_font('dejavu', '', os.path.join(FONT_PATH, 'DejaVuSans.ttf'), uni=True)

    pdf.set_font('dejavu', size=20)
    pdf.set_text_color(5, 14, 110)
    pdf.cell(200, 10, txt=f'RSS News', ln=1, align="C")
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)

    for new in all_news:
        add_new_to_pdf(cmd_args, new, pdf, logger)

    logger.info(f'Download PDF file with required news to the {path_to_pdf}')

    try:
        pdf.output(path_to_pdf, 'F')
    except FileNotFoundError:
        raise PATHError('Setted PATH is invalid')


def add_new_to_pdf(cmd_args, new, pdf, logger):
    """
    Add one new to PDF file
    """
    pdf.set_font_size(16)
    pdf.set_text_color(84, 10, 10)
    pdf.multi_cell(200, 8, txt=new.get('title'))
    pdf.ln(5)
    pdf.set_font_size(10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 5, txt=new.get('date'))
    pdf.ln(10)
    pdf.set_font_size(11)
    pdf.set_text_color(0, 0, 128)
    pdf.write(6, 'Link to the full article', new.get('link'))
    pdf.set_text_color(0, 0, 0)
    pdf.set_font_size(12)
    pdf.ln(10)

    if not cmd_args.date:
        logger.info('Add image(s) from the received links to the file')

        for num, link in enumerate(new.get('img_link'), 1):
            if link:
                add_downloaded_image(num, link, pdf, logger)
    else:
        pdf.cell(200, 8, txt='Links to the image(s): ')
        pdf.ln(8)
        for num, link in enumerate(new.get('img_link'), 1):
            add_image_link(num, link, pdf)

    pdf.ln(5)
    pdf.set_font_size(12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(200, 8, txt=new.get('text'))
    pdf.ln(10)


def add_downloaded_image(num, link, pdf, logger):
    """
    Download image, add it to PDF file and delete it
    """
    logger.info(f'Download image № {num} from {link} from received URL.')

    (filename, headers) = urllib.request.urlretrieve(link)
    image_format = headers['content-type'].replace('image/', '')

    if image_format not in ('jpeg', 'png'):
        logger.info(f"Image № {num} from {link} is not in an appropriate format.")
        add_image_link(num, link, pdf)
    else:
        logger.info(f"Format of image № {num} from {link} is appropriate.")

        pdf.image(filename, x=70, y=pdf.get_y(), h=40, type=image_format, link=link)
        pdf.ln(40)

        logger.info(f'Delete downloaded image № {num} from {link}.')
        os.remove(filename)


def add_image_link(num, link, pdf):
    """
    Add image link to the PDF file
    """
    pdf.set_text_color(0, 0, 128)
    pdf.set_font_size(11)
    pdf.write(8, f'Link to the image № {num}', link)
    pdf.ln(6)
