"""This module converts data to pdf"""

from fpdf import FPDF
import urllib.request as url
import os
import sys
import datetime
import re

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
FONT = 'ARIALUNI.TTF'

WIN_FONT = r'C:\Windows\Fonts\arial.ttf'
LIN_FONT = r'/usr/share/fonts/dejavu/DejaVuSansCondensed.ttf'

if sys.platform == 'win32':
    if os.path.isfile(WIN_FONT):
        FONTPATH = WIN_FONT
    else:
        FONTPATH = os.path.join(THIS_DIRECTORY, FONT)

if sys.platform == 'linux':
    if os.path.isfile(LIN_FONT):
        FONTPATH = LIN_FONT
    else:
        FONTPATH = os.path.join(THIS_DIRECTORY, FONT)


def convert_pdf(rss_news_clean: dict, path: str):
    """This function creates pdf"""

    date_time = datetime.datetime.now()

    pdf = FPDF()
    pdf.add_font('arial_uni', '', FONTPATH, True)
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
                create_image_template(pdf)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n IMAGE IS CORRUPTED')
            except url.HTTPError:
                create_image_template(pdf)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n IMAGE IS CORRUPTED')
            except url.URLError:
                create_image_template(pdf)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n NO INTERNET CONNECTION')
            except ValueError:
                create_image_template(pdf)
                pdf.multi_cell(w=50, h=12, align='C', txt=' \n NO PICTURE AVAILABLE')

        else:
            create_image_template(pdf)
            pdf.multi_cell(w=50, h=12, align='C', txt=' \n NO PICTURE AVAILABLE')

        pdf.set_font("arial_uni", size=12)

        title_string = str(rss_news['title'].encode('utf-8', 'ignore').decode('utf-8'))
        feed_string = str(rss_news['feed'].encode('utf-8', 'ignore').decode('utf-8'))
        news_string = str(rss_news['description'].encode('utf-8', 'ignore').decode('utf-8'))

        # The most common problematic character of unicode
        if '&#39;' in title_string:
            title_string = re.sub('&#39;', "'", title_string)

        if '&quot;' in title_string:
            title_string = re.sub('&quot;', "'", title_string)

        if '&#39;' in feed_string:
            feed_string = re.sub('&#39;', "'", feed_string)

        if '&#39;' in news_string:
            news_string = re.sub('&#39;', "'", news_string)

        if '&quot;' in news_string:
            news_string = re.sub('&quot;', "'", news_string)

        string = 'Feed: ' + feed_string + '\n' + '   ' + '\n' 'Title: ' + title_string + '\n' + '   ' + '\n'
        string += 'Date: ' + rss_news['date'] + '\n' + '   ' + '\n'
        pdf.multi_cell(w=100, h=6, txt=string)

        pdf.set_font("arial_uni", size=12)
        string = 'News: ' + '\n' + '   \n\n' + news_string
        pdf.write(h=6, txt=string)

        pdf.set_font("Arial", "B", size=12)
        pdf.write(h=6, txt='Link: ' + rss_news['link'], link=rss_news['link'])

    pdf.output(path + 'news' + date_time.strftime("%Y%m%d-%H-%M-%S") + '.pdf', 'F')


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


def convert_html(rss_news_clean: dict, path: str):
    """This function creates html"""

    date_time = datetime.datetime.now()

    with open(path+'news' + date_time.strftime("%Y%m%d-%H-%M-%S") + '.html', 'w+', encoding='utf-8') as file:
        file.write('<html>')
        file.write('<head>')
        file.write('<title> News for ' + date_time.strftime("%Y.%m.%d - %H:%M:%S") + '</title>')
        file.write('</head>')
        file.write('<body>')

        for rss_news in rss_news_clean.values():

            title_string = str(rss_news['title'].encode('utf-8', 'ignore').decode('utf-8'))
            news_string = str(rss_news['description'].encode('utf-8', 'ignore').decode('utf-8'))

            # The most common problematic character of unicode
            if '&#39;' in title_string:
                title_string = re.sub('&#39;', "'", title_string)

            if '&quot;' in title_string:
                title_string = re.sub('&quot;', "'", title_string)

            if '&#39;' in news_string:
                news_string = re.sub('&#39;', "'", news_string)

            if '&quot;' in news_string:
                news_string = re.sub('&quot;', "'", news_string)

            file.write('<div <h1><b> ')
            file.write(title_string + ' </b></h1></br></br>')
            file.write('<div<p><b>' + rss_news['date'] + '</b></p></div>')
            file.write(' <div <p>' + news_string + ' </p> </div>')

            if rss_news['image'] is not None:
                file.write('<div> ' + '<img src=' + rss_news['image'] + ' width="200" height="120"> </div>')
            else:
                file.write('<div<p><b> Image is not available</b></p></div>')

            file.write('<div <p> Link: <a href=' + rss_news['link'] + '>' + rss_news['link'] + '</a></p> </div>')
            file.write('</div>')
            file.write('</br></br></br>')

        file.write('</body> </html>')


def convert_log_html(log_journal: dict, path: str):
    """This function converts log to html"""

    with open(path+'log.html', 'w+', encoding='utf-8') as file:
        file.write('<html>')
        file.write('<head>')
        file.write('<title> Log journal output </title>')
        file.write('</head>')
        file.write('<body>')

        for line in log_journal.values():
            file.write('<h1><b>' + line + '</b></h1>')

        file.write('</body> </html>')


def create_image_template(pdf):
    """This function creates image template"""

    pdf.set_line_width(1)
    pdf.rect(120, 12, 50, 50)
    pdf.set_xy(120, 12)
    pdf.set_font("Arial", "B", size=14)
