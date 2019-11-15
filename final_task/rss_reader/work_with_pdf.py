import os
import datetime
from fpdf import FPDF
import requests


def write_to_pdf_file(data: dict, path: str):
    if os.path.isdir(path):
        date_str = datetime.datetime.now().date().strftime('%Y%m%d')
        filename = path + os.path.sep + date_str + '_' + data['title'][:data['title'].find(' ')].replace(':', '').replace('.', '') + '.pdf'
        pdf = FPDF()
        effective_page_width = pdf.w - 2 * pdf.l_margin
        pdf.compress = False
        pdf.add_page()
        pdf.add_font("my", '', '18223.ttf', uni=True)
        pdf.set_font("my", size=30)
        pdf.cell(w=0, txt=data['title'])
        pdf.set_font("my", size=20)
        pdf.ln(30)
        pdf.set_line_width(1)
        pdf.set_draw_color(255, 0, 0)
        for index_news, news_dict in enumerate(data['items']):
            pdf.line(20, pdf.get_y() - 10, effective_page_width, pdf.get_y() - 10)
            pdf.multi_cell(effective_page_width, 10, news_dict['title'])
            if news_dict['summary'][0] == '[' and data['links'][index_news]:
                p = requests.get(data['links'][index_news])
                if p.status_code == 200 and data['links'][index_news].find('.gif') == -1:
                    out = open('img' + str(index_news) + '.jpg', "wb")
                    out.write(p.content)
                    out.close()
                    try:
                        pdf.image('img' + str(index_news) + '.jpg')
                    except RuntimeError:
                        image_str = news_dict['summary'][
                                    news_dict['summary'].find(':') + 1:news_dict['summary'].find(']')]
                        pdf.multi_cell(effective_page_width, 10, image_str)
                    os.remove('img' + str(index_news) + '.jpg')
                else:
                    image_str = news_dict['summary'][news_dict['summary'].find(':') + 1:news_dict['summary'].find(']')]
                    pdf.multi_cell(effective_page_width, 10, image_str)
            pdf.multi_cell(effective_page_width, 10, news_dict['published'])
            pdf.multi_cell(effective_page_width, 10, news_dict['summary'][news_dict['summary'].rfind(']') + 2:])
            pdf.ln(40)
        try:
            pdf.output(filename, 'F')
        except PermissionError:
            return f'close file:\n{filename}'


        return f'the recording has been completed in the file:\n{filename}'
    else:
        return f'{path} is not found'



