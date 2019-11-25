
from dominate.tags import div, h2, img, p, a, meta
from datetime import datetime
import dominate
import html
import os
import httplib2
import socket
from colorizer import printerr
from fpdf import FPDF

def is_connected() -> bool:
    try:
        socket.create_connection(("www.google.com", 80))
    except Exception:
        return False
    return True


def font_decorator(function_to_decorate):
    """
    The wrapper takes the function that sets the font
    and applies this font to the text
    """
    def wrapper(text, page, font):
        function_to_decorate(text, page, font)
        if font == 'Arial':
            page.cell(1, 1, text + '\n')
        else:
            page.multi_cell(w=100, h=6, txt='\n' + text + '\n\n', align='L')
    return wrapper


@font_decorator
def font_print(text, page, font):
    """
    Sets a font on a page
    Has a text argument to have a possibility to be wrapped
    """
    if font == 'Arial':
        page.set_font(font, 'B', size=12)
    else:
        page.set_font(font)


def pdf_convert(news, limit, path, color):
    """
    Converts news into pdf format using FPDF library
    Caching is used to fasten images loading(httplib2 library)
    """
    pdf = FPDF()
    count = 0
    h = httplib2.Http('.cache')
    pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
    for ind, item in enumerate(news[slice(None, limit)]):
        pdf.add_page()
        count_on_page = -1
        if is_connected():
            for image in item['image']:
                count_on_page += 1
                if count_on_page > 4:
                    break
                count += 1
                position = count_on_page * 52 + 12
                try:
                    response, content = h.request(image)
                    out = open('image' + str(count) + '.jpg', 'wb')
                    out.write(content)
                    out.close()
                    pdf.image('image' + str(count) + '.jpg', 130, position, 70, 50)
                except Exception:
                    pass
        font_print('Title', pdf, 'Arial')
        font_print(item['title'], pdf, 'FreeSans')
        font_print('Date', pdf, 'Arial')
        date = datetime.strptime(item['date'][:-6], '%a, %d %b %Y %H:%M:%S').strftime("%A, %d %B %Y, %H:%M:%S")
        font_print(str(date), pdf, 'FreeSans')
        font_print('Link', pdf, 'Arial')
        font_print(item['link'], pdf, 'FreeSans')
        if not is_connected():
            text = '\n'
            font_print('Images', pdf, 'Arial')
            for image in item['image']:
                text += image + '\n'
            text += '\n'
            pdf.set_font("FreeSans", size=8)
            pdf.multi_cell(w=100, h=4, txt=text, align='L')
        font_print('Description', pdf, 'Arial')
        if len(item['description']) > 9000:
            font_size = 6
        elif len(item['description']) > 5000:
            font_size = 7
        elif len(item['description']) > 3000:
            font_size = 8
        if len(item['description']) > 3000 and count_on_page < 1:
            pdf.set_font("FreeSans", size=font_size)
            pdf.multi_cell(w=190, h=4, txt='\n' + item['description'])
        else:
            font_print(item['description'], pdf, 'FreeSans')
    try:
        if not os.path.exists(path):
            os.path.join(path)
        time_name = datetime.strftime(datetime.now(), "%d-%m-%y-%H-%M")
        filename = time_name + '.pdf'
        filename = os.path.join(path, filename)
        pdf.output(filename)
    except FileNotFoundError:
        printerr('Wrong path to pdf file', color)

    for num in range(1, count + 1):
        try:
            os.remove('image' + str(num) + '.jpg')
        except FileNotFoundError:
            pass


def html_convert(news, limit, path, color):
    """
    Converts news into html format using tags from dominate library
    FreeSans font enables to show cyrillic in the right way
    """
    doc = dominate.document(title='News')
    for ind, item in enumerate(news[slice(None, limit)]):
        with doc:
            meta(charset='utf-8')
            with div():
                h2(html.unescape(item['title']))
                date = datetime.strptime(item['date'][:-6], '%a, %d %b %Y %H:%M:%S').strftime("%A, %d %B %Y, %H:%M:%S")
                p(str(date))
                p(item['description'])
                p(a('Link', href=item['link']))
                if item['image']:
                    if is_connected():
                        for image in item['image']:
                            img(src=image, width="500", height="auto", alt=item['title'])
                    else:
                        p('Images:')
                        imgstr = ''
                        for image in item['image']:
                            imgstr += image + '\n'
                        p(imgstr)
    try:
        if not os.path.exists(path):
            os.path.join(path)
        time_name = datetime.strftime(datetime.now(), "%d-%m-%y-%H-%M")
        filename = time_name + '.html'
        filename = os.path.join(path, filename)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(doc))
    except FileNotFoundError:
        printerr('Wrong path to html file', color)
