
from dominate.tags import div, h2, img, p, a, meta, head
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
    def wrapper(text, page, font):
        function_to_decorate(text, page, font)
        if font == 'Arial':
            page.cell(1, 1, text + '\n')
        else:
            page.multi_cell(w=100, h=6, txt=text, align='L')
    return wrapper


@font_decorator
def font_print(text, page, font):
    if font == 'Arial':
        page.set_font(font, 'B', size=12)
    else:
        page.set_font(font)


def pdf_convert(news, limit, path, color):
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
        text = '\n' + item['title'] + '\n\n'
        font_print(text, pdf, 'FreeSans')
        font_print('Date', pdf, 'Arial')
        date = datetime.strptime(item['date'][:-6], '%a, %d %b %Y %H:%M:%S').strftime("%A, %d %B %Y, %H:%M:%S")
        text = '\n' + str(date) + '\n\n'
        font_print(text, pdf, 'FreeSans')
        font_print('Link', pdf, 'Arial')
        text = '\n' + item['link'] + '\n\n'
        font_print(text, pdf, 'FreeSans')
        if not is_connected():
            text = '\n'
            font_print('Images', pdf, 'Arial')
            for image in item['image']:
                text += image + '\n'
            text += '\n'
            pdf.set_font("FreeSans", size=8)
            pdf.multi_cell(w=100, h=4, txt=text, align='L')
        font_print('Description', pdf, 'Arial')
        text = '\n' + item['description']
        if len(text) > 1500 and count_on_page < 1:
            pdf.set_font("FreeSans", size=6)
            pdf.multi_cell(w=190, h=4, txt=text)
        else:
            font_print(text, pdf, 'FreeSans')
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
