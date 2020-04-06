from json import dumps as jdumps
from dataclasses import asdict
from fpdf import FPDF
from os import remove, path
import imghdr
import requests


def news_as_json_str(item_group):
    """ Convert news in json format

    :type item_group: 'item_group.ItemGroup'
    :rtype: str
    """
    news_dict = asdict(item_group)

    return jdumps(news_dict, indent=4, ensure_ascii=False)


def news_as_json_str_from_list(item_groups):
    """ Convert list of news in json format

    :type item_groups: list of 'item_group.ItemGroup'
    :rtype: str
    """
    lst = [asdict(item_gr) for item_gr in item_groups]

    return jdumps(lst, indent=4, ensure_ascii=False)


def news2html(item_groups):
    """ Convert news to HTML code

    :type item_groups: list of 'item_group.ItemGroup'
    :return: HTML code
    :rtype: str
    """
    green_line = '<hr align=center size=3 width=70% color=green>'
    font = '../fonts/DejaVuSansCondensed.ttf'

    html_code = '<html><head><title>News</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type">' \
                '<style>@font-face {font-family: DejaVuSans;src: url("' + font + '");}' \
                'body {font-family: DejaVuSans;}</style></head><body>_content_</body></html>'

    content = ''

    for item_gr in item_groups:
        item_gr_html = '<div>' + green_line + '<h1 align=center>' + item_gr.feed + '</h1>' + green_line + \
                       '<div>' + items2html(item_gr.items) + '</div></div>'
        content += item_gr_html

    html_code = html_code.replace('_content_', content)

    return html_code


def items2html(items):
    """ Convert items to HTML code

    :type items: list of 'item.Item'
    :return: HTML code
    :rtype: str
    """
    black_line = '<hr align=center size=1 width=70% color=black>'
    source_link_text = 'Go to source..'
    items_html = ''

    for item in items:
        itm_html = '<div style="margin: 60px 15% 20px 15%;"><h3 align=center>' + item.title + '</h3>' + \
                    '<p align="justify">' + item_text_with_imgs2html(item.text, item.img_links) + '</p>' + \
                    '<br><small><i><a href=' + item.link + ' color=blue>' + source_link_text + '</a><br>' + \
                    '<span style="float:right; margin-right:90">' + str(item.date) + '</span></i></small><br></div>'

        items_html += itm_html + black_line

    items_html = items_html[:-len(black_line)]
    return items_html


def item_text_with_imgs2html(text, img_links):
    """ Convert text with images to HTML code

    :type text: str
    :type img_links: list of str

    :return: HTML code
    :rtype: str
    """
    text_and_imgs = ''

    for ind, link in enumerate(img_links):
        alt, before_picture, text = parse_item_text(text, ind + 1)

        if before_picture:
            text_and_imgs += before_picture

        text_and_imgs += '<p style="text-align: center;">' \
                         '<img src="' + link + '" alt="' + alt + '" style="margin-bottom: 30px;"></p>'

    text_and_imgs += text
    return text_and_imgs


def news2pdf(item_groups, file_path):
    """ Write news in PDF file

    :type item_groups: list of 'item_group.ItemGroup'
    :type file_path: str
    """
    width = 180

    pdf = FPDF()
    pdf.add_page()

    current_dir = path.dirname(path.abspath(__file__))
    fonts_dir = current_dir[:current_dir.find('EGG-INFO')] + path.join('rss_reader', 'fonts')

    pdf.add_font('DejaVu', '', path.join(fonts_dir, 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.add_font('DejaVuBold', '', path.join(fonts_dir, 'DejaVuSansCondensed-Bold.ttf'), uni=True)
    pdf.add_font('DejaVuOblique', '', path.join(fonts_dir, 'DejaVuSansCondensed-Oblique.ttf'), uni=True)

    num = 0

    for item_gr in item_groups:
        pdf.set_font('DejaVuBold', size=24)
        pdf.set_text_color(0, 10, 180)
        pdf.multi_cell(width, 260, item_gr.feed, align='C')

        for item in item_gr.items:
            pdf.add_page()

            pdf.set_font('DejaVuBold', size=18)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(width, 16, item.title, align='C')

            pdf.set_font('DejaVu', size=16)

            text = item.text
            for ind, link in enumerate(item.img_links):
                alt, before_picture, text = parse_item_text(text, ind+1)

                if before_picture:
                    pdf.multi_cell(width, 16, before_picture)

                try:
                    img = requests.get(link)
                    if img.status_code != 200 or imghdr.what(None, img.content) != 'jpeg':
                        raise requests.exceptions.ConnectionError()

                except requests.exceptions.ConnectionError:
                    pdf.set_font('DejaVuOblique', size=14)
                    pdf.set_text_color(80, 80, 80)

                    pdf.multi_cell(width, 14, f'[image: {alt}][{link}]')

                    pdf.set_font('DejaVu', size=16)
                    pdf.set_text_color(0, 0, 0)
                else:
                    file_image_name = str(num) + 'tmp_img.jpg'

                    with open(file_image_name, 'wb') as img_file:
                        img_file.write(img.content)

                    pdf.multi_cell(width, 16, '')
                    pdf.image(file_image_name, x=75)
                    pdf.multi_cell(width, 16, '')

                    remove(file_image_name)
                    num += 1

            pdf.multi_cell(width, 16, text)

            pdf.set_font('DejaVuOblique', size=11)
            pdf.set_text_color(0, 0, 255)
            pdf.multi_cell(width, 11, '')
            pdf.cell(width, 11, 'Go to source...', link=item.link)

            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(width, 11, '')
            pdf.multi_cell(width, 11, str(item.date))

        pdf.multi_cell(width, 16, '')

    pdf.output(file_path)


def parse_item_text(text, img_num):
    """ Return alternative text of image, text before image and text after image

    :rtype: tuple of str
    """
    img_begin = text.find(f'[image {img_num}:')
    img_end = text.find(f'[{img_num}]', img_begin) + len(str(img_num)) + 2

    len_num = len(str(img_num))
    alt = text[img_begin + len_num + 9:img_end - len_num - 3]

    before_picture = text[:img_begin]
    after_picture = text[img_end:]

    return alt, before_picture, after_picture
