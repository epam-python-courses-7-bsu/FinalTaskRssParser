import os
import datetime
from fpdf import FPDF
import requests
import RssReaderException


def write_to_pdf_file(data: dict, path: str):
    if os.path.isdir(path):
        date_str = datetime.datetime.now().date().strftime('%Y%m%d')
        date_str += '_' + data['title'][:data['title'].find(' ')].replace(':', '').replace('.', '')
        filename = os.path.join(path, date_str + '.pdf')
        write_to_pdf(data, filename)
        return f'The recording has been completed in the file:\n{filename}'
    else:
        raise RssReaderException.FileException(f'{path} is not found')


def write_to_pdf(data: dict, filename: str):
    pdf = FPDF()
    effective_page_width = pdf.w - 2 * pdf.l_margin
    pdf.compress = False
    pdf.add_page()
    pdf.add_font("TimesNewRoman", '', 'TimesNewRoman.ttf', uni=True)
    pdf.set_font("TimesNewRoman", size=30)
    pdf.cell(w=0, txt=data['title'])
    pdf.ln(30)
    pdf.set_line_width(1)
    pdf.set_draw_color(255, 0, 0)
    for index_news, news_dict in enumerate(data['items']):
        pdf.set_font("TimesNewRoman", size=20)
        pdf.line(20, pdf.get_y() - 10, effective_page_width, pdf.get_y() - 10)
        pdf.multi_cell(effective_page_width, 10, news_dict['title'])
        if news_dict['contain_image']:
            download_image_and_paste_in_pdf(pdf, news_dict, index_news)
        pdf.multi_cell(effective_page_width, 10, news_dict['published'])
        pdf.multi_cell(effective_page_width, 10, news_dict['summary'][news_dict['summary'].rfind(']') + 1:])
        pdf.set_font("TimesNewRoman", size=15)
        pdf.ln(5)
        pdf.multi_cell(effective_page_width, 10, 'Link on news:\n' + news_dict['link'])
        if news_dict['contain_image']:
            pdf.multi_cell(effective_page_width, 10, 'Link on image:\n' + news_dict['link_on_image'])
        pdf.ln(40)
    try:
        pdf.output(filename, 'F')
    except PermissionError:
        raise RssReaderException.FileException(f'close file:\n{filename}')


def download_image_and_paste_in_pdf(pdf, news_dict: dict, index_news: int):
    effective_page_width = pdf.w - 2 * pdf.l_margin
    try:
        p = requests.get(news_dict['link_on_image'])
        if p.status_code == 200 and news_dict['link_on_image'].find('.gif') == -1:
            with open('img' + str(index_news) + '.jpg', "wb") as out:
                out.write(p.content)
            try:
                pdf.image('img' + str(index_news) + '.jpg')
            except RuntimeError:
                # image_str - alternative text for image
                image_str = 'Image:' + news_dict['summary'][news_dict['summary'].find(':') + 1:
                                                            news_dict['summary'].find(']')]
                pdf.multi_cell(effective_page_width, 10, image_str)
            os.remove('img' + str(index_news) + '.jpg')
        else:
            image_str = 'Image:' + news_dict['summary'][news_dict['summary'].find(':') + 1:
                                                        news_dict['summary'].find(']')]
            pdf.multi_cell(effective_page_width, 10, image_str)
    except requests.exceptions.ConnectionError:
        image_str = 'Image:' + news_dict['summary'][news_dict['summary'].find(':') + 1:
                                                    news_dict['summary'].find(']')]
        pdf.multi_cell(effective_page_width, 10, image_str)
