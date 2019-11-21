from PIL import Image
import requests
import base64
from io import BytesIO
import os
import logging
from parse_rss_functions import ckeck_internet


def get_new_content_html(new):
    """
    :param new: The new
    :return:  string representation of new in html
    Converts new into string which will be used in html format
    """
    images_content = ""
    if not ckeck_internet():
        for image_link in new['Image links']:
            images_content += f"<a href=\"{image_link}\">{image_link}</a>"
    else:
        for image_link in new['Image links']:
            if image_link == "":
                continue
            response = requests.get(image_link)
            encoded_string = str(base64.b64encode(response.content))
            images_content += "<img width=200 height=200 src=\"data:image/jpeg;base64," + encoded_string[2:len(
                encoded_string) - 1] + "\"/>\n"
    return f"""
    <p>{new['Feed']}</p>
    <p>{new['Title']}</p>
    <p>{new['Date']}</p>
    <p><a href="{new['Link']}">{new['Link']}</a></p>
    <p>{images_content}</p>
    <p>{new['New description']}</p>
    <br><br>
    """


def save_in_html(path, news_list):
    """
    :param path: The path of html format file
    :param news_list: The list of news
    Saves news in html format by path
    """
    logging.info('Creating html format file')
    html_content = "<html>\n<body>\n"
    for new in news_list:
        html_content += get_new_content_html(new)
    html_content += "</body>\n</html>"
    with open(path, 'w', encoding="utf-8") as html_file:
        html_file.write(html_content)
    logging.info('Html format file created')


def get_new_content_fb2(new):
    """
    :param new: The new
    :return:  string representation of new in fb2
    Converts new into string which will be used in fb2 format
    """
    images_content = ""
    for image_link in new['Image links']:
        images_content += f"<image xlink:href=\"#{image_link}\" />"
    return f"""
<section>
    <p>{new['Feed'].replace('&', 'and')}</p>
    <p>{new['Title'].replace('&', 'and')}</p>
    <p>{new['Date']}</p>
    <p>{images_content}</p>
    <p>{new['New description'].replace('&', 'and')}</p>
</section>
    """


def get_images_content(news_list):
    """
    :param news_list: The list of news
    :return: string representation of images
    Transforms images into string by using base64
    """
    if not ckeck_internet():
        return ""
    images_content = ""
    for new in news_list:
        for image_link in new['Image links']:
            if image_link == "":
                continue
            response = requests.get(image_link)
            img = Image.open(BytesIO(response.content))
            img = img.resize((100, 100))
            img = img.convert('RGB')
            img.save('tmp.jpg', 'JPEG')
            with open('tmp.jpg', 'rb') as f:
                encoded_string = str(base64.b64encode(f.read()))
            images_content += f"<binary id=\"{image_link}\" content-type=\"image/jpeg\">\n" + encoded_string[2:len(
                encoded_string) - 1] + "\n</binary>\n"
    os.remove('tmp.jpg')
    return images_content


def save_in_fb2(path, news_list):
    """
     :param path: The path of fb2 format file
     :param news_list: The list of news
     Saves news in fb2 format by path
     """
    logging.info('Creating fb2 format file')
    fb2_content = """<?xml version="1.0" encoding="utf-8"?>
            <FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>"""
    for new in news_list:
        fb2_content += get_new_content_fb2(new)
    fb2_content += "\n</body>\n"
    fb2_content += get_images_content(news_list) + "</FictionBook>"
    with open(path, 'w', encoding="utf-8") as fb2_file:
        fb2_file.write(fb2_content)
    logging.info('Fb2 format file created')
