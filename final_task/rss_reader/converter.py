
from dominate.tags import div, h2, img, p, a
from datetime import datetime
import dominate
import html
import os
import httplib2
import socket

from fpdf import FPDF


def is_connected() -> bool:
    try:
        socket.create_connection(("www.google.com", 80))
    except Exception:
        return False
    return True


def pdf_convert(news, limit, path):
    pdf = FPDF()
    count = 0
    h = httplib2.Http('.cache')
    pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
    for ind, item in enumerate(news):
        if ind + 1 > limit:
            print('dima')
            break
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
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(1, 1, 'Title:\n')
        pdf.set_font("FreeSans")
        string = '\n' + item['title'] + '\n\n'
        pdf.multi_cell(w=100, h=6, txt=string, align='L')
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(1, 1, 'Date:\n')
        pdf.set_font("FreeSans")
        date = datetime.strptime(item['date'][:-6], '%a, %d %b %Y %H:%M:%S').strftime("%A, %d %B %Y, %H:%M:%S")
        string = '\n' + str(date) + '\n\n'
        pdf.multi_cell(w=100, h=6, txt=string, align='L')
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(1, 1, 'Link:\n')
        string = '\n' + item['link'] + '\n\n'
        pdf.multi_cell(w=100, h=6, txt=string, align='L')
        if not is_connected():
            string = '\n'
            pdf.cell(1, 1, 'Images:\n')
            for image in item['image']:
                string += image + '\n'
            string += '\n'
            pdf.set_font("FreeSans", size=8)
            pdf.multi_cell(w=100, h=4, txt=string, align='L')
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(1, 1, 'Description:\n')
        string = '\n' + item['description']
        if len(string) > 3000 and count_on_page < 1:
            pdf.set_font("FreeSans", size=6)
            pdf.multi_cell(w=190, h=4, txt=string)
        else:
            pdf.set_font("FreeSans")
            pdf.multi_cell(w=100, h=4, txt=string, align='L')
    if not os.path.exists(path):
        os.path.join(path)
    time_name = datetime.strftime(datetime.now(), "%d-%m-%y-%H-%M")
    filename = path + '/' + time_name + '.pdf'
    pdf.output(filename)

    for num in range(1, count + 1):
        try:
            os.remove('image' + str(num) + '.jpg')
        except FileNotFoundError:
            pass


def html_convert(news, limit, path):
    doc = dominate.document(title='News')
    for ind, item in enumerate(news):
        if ind == limit:
            break
        with doc:
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
    if not os.path.exists(path):
        os.path.join(path)
    time_name = datetime.strftime(datetime.now(), "%d-%m-%y-%H-%M")
    filename = path + '/' + time_name + '.html'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(doc))
