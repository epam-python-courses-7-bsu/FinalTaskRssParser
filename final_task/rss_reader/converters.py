import datetime
import logging
import os

import requests
from dominate import document
from dominate.tags import *
from fpdf import FPDF

from exceptions_ import ConvertionError

LOGGER = logging.getLogger('rss_logger')


def path_validation(path, mode):
    '''
    Raises an exception if the path is not valid
    Otherwise returns path

    Mode is boolean to determine file extention
    True - .html
    False - .pdf
    '''
    get_extention = (lambda mode: '.html' if mode else '.pdf')
    LOGGER.debug('CHECKING PATH')
    if path.endswith('/'):
        path += 'feed-' + str(datetime.datetime.now()) + get_extention(mode)
    else:
        path += '/feed-' + str(datetime.datetime.now()) + get_extention(mode)
    try:
        LOGGER.debug('TRYING TO CREATE FILE...')
        export_file = open(path, 'w', encoding='utf-8')
        export_file.close()
        LOGGER.debug('PATH IS OK')
        return path
    except FileNotFoundError as exc:
        raise ConvertionError('Wrong path')


def get_html_doc(news_list):
    '''
    Converts news to .html

    news_list - is a list of dicts
    '''
    LOGGER.debug('CONVERTING TO HTML')
    with document(title='RSS FEED') as doc:
        h1('News:')
        for news_item in news_list:
            with div():
                h3(news_item['title'])
                h5('IMAGE')
                LOGGER.debug('PROCESSING IMAGE')
                if news_item['img'] is None:
                    p('NO IMAGE')
                else:
                    # Image is stored in base64. It's needed to skip first 2 and
                    # the last chars to take valid_base64_string because it's stored as
                    # b'valid_base64_string'
                    img(src='data:image/png;base64, ' + str(news_item['img'])[2:-1])
                LOGGER.debug('DONE')
                h5('DESCRIPTION: ')
                p(news_item['description'])
                p(news_item['published'])
                p('SOURCE: ' + news_item['source'])
                a('LINK', href=news_item['link'])
    return str(doc)


def to_html(path, item_list):
    try:
        path = path_validation(path, True)
    except ConvertionError as exc:
        raise exc
    document = get_html_doc(item_list)
    LOGGER.debug('WRITING .html')
    with open(path, 'w', encoding='utf-8') as html_file:
        html_file.write(str(document))


def get_image_path(url):
    '''
    FPDF can't handle image in base64
    The function tries to take the image from the source
    If it does it create temp-img file and returns path
    to it
    If it doesn't it raises an requests.ConnectionError
    exception which handled in Image adding section
    '''
    LOGGER.debug('GETTING IMAGE FROM URL...')
    temp_img = 'temp-img' + str(hash(url)) + '.jpg'
    img = requests.get(url).content
    with open(temp_img, 'wb') as img_out:
        img_out.write(img)
    LOGGER.debug('DONE')
    return temp_img


def get_pdf_doc(news_list):
    '''
    Converts news to .pdf

    news_list - is a list of dicts
    '''
    LOGGER.debug('CONVERTING TO PDF')
    pdf = FPDF(format='A4')
    LOGGER.debug('SETIING FONTS')
    pdf.add_font("NotoSans", style="", fname="NotoSans-Black.ttf", uni=True)
    pdf.add_font("NotoSans", style='B', fname="NotoSans-Bold.ttf", uni=True)
    pdf.set_font("NotoSans", 'B', size=24)
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.cell(50, 30, txt='News Feed:', ln=1, align='L')
    for news_item in news_list:
        pdf.set_font("NotoSans", '', size=12)
        pdf.set_x(4)
        pdf.cell(20, 6, 'Title:', ln=1)
        pdf.set_font("NotoSans", '', size=12)
        pdf.set_x(20)
        pdf.multi_cell(150, 5, news_item['title'])
        pdf.set_x(4)
        pdf.set_font("NotoSans", '', size=12)
        pdf.cell(20, 6, 'Image:', ln=1)
        # Image adding
        LOGGER.debug('IMAGE ADDING')
        if news_item['img'] is None:
            LOGGER.debug('IMAGE IS NONE')
            pdf.set_font("NotoSans", '', size=12)
            pdf.set_x(20)
            pdf.cell(20, 6, 'No image', ln=1)
            pdf.set_x(4)
        else:
            try:
                img_path = get_image_path(news_item['media'])
                pdf.image(img_path, x=20)
                os.remove(img_path)
            except (requests.Timeout, requests.TooManyRedirects, requests.ConnectionError) as exc:
                print(str(exc))
                pdf.set_x(20)
                pdf.multi_cell(150, 6, str(exc))
            except Exception as exc:
                print(str(exc))
                pdf.set_x(20)
                pdf.multi_cell(150, 6, 'Image error')
                os.remove(img_path)
        # End image adding
        pdf.set_x(4)
        pdf.cell(20, 6, 'Description:', ln=1)
        pdf.set_x(20)
        if len(news_item['description']) == 0:
            pdf.multi_cell(150, 5, news_item['title'])
        else:
            pdf.multi_cell(150, 5, news_item['description'])
        pdf.set_x(4)
        pdf.cell(20, 6, 'LINK', link=news_item['link'], ln=1)
        pdf.set_x(4)
        pdf.cell(20, 6, 'Source: ' + news_item['source'], link=news_item['source'], ln=1)
        pdf.cell(0, 10, '='*85, align='C', ln=1)
    return pdf


def to_pdf(path, news_list):
    try:
        path = path_validation(path, False)
    except ConvertionError as exc:
        raise exc
    pdf = get_pdf_doc(news_list)
    LOGGER.debug('SAVING .pdf')
    pdf.output(path)
    LOGGER.debug('DONE!')
