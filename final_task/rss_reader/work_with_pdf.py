import os
import datetime
from fpdf import FPDF
import requests
import MyException


def write_to_pdf_file(data: dict, path: str):
    if os.path.isdir(path):
        date_str = datetime.datetime.now().date().strftime('%Y%m%d')
        filename = os.path.join(path, date_str + '_' +
                                data['title'][:data['title'].find(' ')].replace(':', '').replace('.', '') + '.pdf')
        write_to_pdf(data, filename)
        return f'The recording has been completed in the file:\n{filename}'
    else:
        raise MyException.MyException(f'{path} is not found')


def write_to_pdf(data: dict, filename: str):
    pdf = FPDF()
    effective_page_width = pdf.w - 2 * pdf.l_margin
    pdf.compress = False
    pdf.add_page()
    pdf.add_font("my", '', '18223.ttf', uni=True)
    pdf.set_font("my", size=30)
    pdf.cell(w=0, txt=data['title'])
    pdf.ln(30)
    pdf.set_line_width(1)
    pdf.set_draw_color(255, 0, 0)
    for index_news, news_dict in enumerate(data['items']):
        pdf.set_font("my", size=20)
        pdf.line(20, pdf.get_y() - 10, effective_page_width, pdf.get_y() - 10)
        pdf.multi_cell(effective_page_width, 10, news_dict['title'])
        if news_dict['summary'][0] == '[' and data['links'][index_news]:
            download_image_and_paste_in_pdf(pdf, data, news_dict, index_news)
        pdf.multi_cell(effective_page_width, 10, news_dict['published'])
        pdf.multi_cell(effective_page_width, 10, news_dict['summary'][news_dict['summary'].rfind(']') + 2:])
        pdf.set_font("my", size=15)
        pdf.ln(5)
        pdf.multi_cell(effective_page_width, 10, 'Link on news:\n' + news_dict['link'])
        pdf.multi_cell(effective_page_width, 10, 'Link on image:\n' + data['links'][index_news])
        pdf.ln(40)
    try:
        pdf.output(filename, 'F')
    except PermissionError:
        raise MyException.MyException(f'close file:\n{filename}')


def download_image_and_paste_in_pdf(pdf, data: dict, news_dict: dict, index_news: int):
    try:
        effective_page_width = pdf.w - 2 * pdf.l_margin
        p = requests.get(data['links'][index_news])
        if p.status_code == 200 and data['links'][index_news].find('.gif') == -1:
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
