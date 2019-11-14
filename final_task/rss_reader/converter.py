"""This module converts data to pdf"""

from fpdf import FPDF
import urllib.request as url
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
font = 'ARIALUNI.ttf'
font_path = os.path.join(this_directory, font)

def convert_pdf(rss_news_clean: dict, path: str):
    """This function creates pdf"""
    pdf = FPDF()
    pdf.add_font('arial_uni', '', font_path, True)
    pdf.set_margins(10, 10, 10)
    counter = 1

    for rss_news in rss_news_clean.values():
        pdf.add_page(('P', 'A4'))

        if rss_news['image']:
            try:
                url.urlretrieve(rss_news['image'], str(counter)+'imageTemp.jpg')
                pdf.image(str(counter)+'imageTemp.jpg', 120, 12, 50, 50, link=rss_news['image'])
                os.remove(str(counter)+'imageTemp.jpg')
                counter += 1
            except RuntimeError:
                pdf.set_line_width(1)
                pdf.rect(120, 12, 50, 50)
                pdf.set_xy(120, 12)
                pdf.set_font("Arial", "B", size=14)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n IMAGE IS CORRUPTED')
            except url.HTTPError:
                pdf.set_line_width(1)
                pdf.rect(120, 12, 50, 50)
                pdf.set_xy(120, 12)
                pdf.set_font("Arial", "B", size=14)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n IMAGE IS CORRUPTED')
        else:
            pdf.set_line_width(1)
            pdf.rect(120, 12, 50, 50)
            pdf.set_xy(120, 12)
            pdf.set_font("Arial", "B", size=14)
            pdf.multi_cell(w=50, h=12, align='C', txt=' \n NO PICTURE AVAILABLE')

        pdf.set_font("arial_uni", size=12)
        string = 'Feed: ' + rss_news['feed'] + '\n' + '   ' + '\n' 'Title: ' + rss_news['title'] + '\n' + '   ' + '\n'
        string += 'Date: ' + rss_news['date'] + '\n' + '   ' + '\n'
        pdf.multi_cell(w=100, h=6, txt=string)

        pdf.set_font("arial_uni", size=12)
        string = 'News: ' + '\n' + '   \n' + str(rss_news['description'].encode('utf-8', 'ignore').decode('utf-8'))
        pdf.write(h=6, txt=string)

        pdf.set_font("Arial", "B", size=12)
        pdf.write(h=6, txt= 'Link: ' + rss_news['link'],link=rss_news['link'])

    pdf.output(path + 'news.pdf', 'F')


def convert_log_pdf(log_journal: dict, path: str):
    """This function converts log journal to pdf"""

    pdf = FPDF()
    pdf.set_font('Arial', 'B', size=14)
    pdf.set_margins(10, 10, 10)
    pdf.add_page(('P', 'A4'))

    pdf.write(h=6, txt='Log journal\n')

    pdf.set_font('Arial', size=10)

    for line in log_journal.values():
        pdf.write(h=6, txt=line)

    pdf.output(path+'log.pdf', 'F')
