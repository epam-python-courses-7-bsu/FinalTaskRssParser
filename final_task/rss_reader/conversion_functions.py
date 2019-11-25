import os
import logging
import requests
from pkg_resources import resource_filename
from yattag import Doc
from fpdf import FPDF
from database_functions import put_into_db
from information_about_news import taking_information_from_feedparser, InfoAboutNews


def get_path(path_to_file, expansion):
    """ Checks if the directory is correct or not"""

    if not os.path.exists(path_to_file):
        print("Invalid directory")
        logging.error("Directory doesn't exist")
        return None
    filename = os.path.join(path_to_file, "news." + expansion)
    logging.debug("Directory exists")
    return filename


def convert_into_html_format(feed, dict_of_args):
    """ Creates html file in specified directory and puts information in database, if it was read from website"""

    # openning html-file to write
    filename = get_path(dict_of_args.get("path"), "html")
    if not filename:
        return None
    file = open(filename, 'w')
    logging.debug("File was opened successfully")

    doc, tag, text, line = Doc().ttl()
    line('h1', 'News from ' + dict_of_args.get("url"))

    for feed_entry in feed:
        # getting list of tags
        if dict_of_args.get("date") is None:
            list_of_tags = taking_information_from_feedparser(feed_entry, dict_of_args)
        else:
            list_of_tags = feed_entry
        news_info = InfoAboutNews(list_of_tags)

        with tag('item'):
            with tag('h2'):
                text(news_info.title)
            with tag('link'):
                text(news_info.link)
            with tag('p'):
                text(news_info.date)
            with tag('h3'):
                if news_info.link_of_img:
                    with tag('img', src=news_info.link_of_img, alt=news_info.link_of_img,
                             border="0", align="left", hspace="5"):
                        pass
                text(news_info.description)
            with tag('br'):
                with tag('br'):
                    pass

        # putting news in database
        if not dict_of_args.get("date"):
            put_into_db(news_info.feed, news_info.title,
                        feed_entry.get("published_parsed", feed_entry.published_parsed),
                        news_info.description, news_info.link, news_info.link_of_img)
    try:
        file.write(doc.getvalue())
        print("News were written in html file")
    except Exception:
        logging.error(Exception)
        print("Can't write information in html file")
    finally:
        file.close()
        return doc.getvalue()


def get_image(link_of_img, count, pdf):
    """ Downloads image from the Internet and puts it into pdf file"""

    try:
        img = requests.get(link_of_img)
        out = open("img" + str(count) + ".jpg", "wb")
        out.write(img.content)
        out.close()
        pdf.image("img" + str(count) + ".jpg", x=100, w=20)
    except requests.exceptions.ConnectionError:
        print("Can't download image, because of connection to the Internet")
        pdf.multi_cell(0, 8, txt=link_of_img, align="C")
        logging.error(requests.exceptions.ConnectionError)
    except Exception as e:
        logging.error("Something wrong with format of image")
        pdf.multi_cell(0, 8, txt=link_of_img, align="C")
        logging.error(e)


def adding_text_in_pdf(pdf, text, size_of_font, indent):
    """ Puts text of specified size in pdf file"""

    pdf.set_font('FreeSans', size=size_of_font)
    pdf.multi_cell(200, indent, txt=(text), align="C")


def get_font(pdf) -> bool:
    """ Gets information about path to font and adds it, if it's possible"""

    pdf.add_font('FreeSans', '', resource_filename(__name__, "ARIALUNI.ttf"), True)
    return True


def convert_into_pdf_format(feed, dict_of_args):
    """ Creates pdf file in specified directory and puts information in database, if it was read from website"""

    filename = get_path(dict_of_args.get("path"), "pdf")
    if not filename:
        return None
    logging.debug("File was opened successfully")

    pdf = FPDF()
    pdf.add_page(('P', 'A4'))
    if not get_font(pdf):
        return None
    pdf.set_margins(10, 10, 10)

    count = 0
    for feed_entry in feed:
        if dict_of_args.get("date") is None:
            list_of_tags = taking_information_from_feedparser(feed_entry, dict_of_args)
        else:
            list_of_tags = feed_entry
        news_info = InfoAboutNews(list_of_tags)

        adding_text_in_pdf(pdf, news_info.title + "\n", 14, 10)
        adding_text_in_pdf(pdf, news_info.date, 10, 8)
        adding_text_in_pdf(pdf, news_info.link, 8, 8)
        if news_info.link_of_img:
            get_image(news_info.link_of_img, count, pdf)
            count += 1
        adding_text_in_pdf(pdf, news_info.description, 10, 6)
        adding_text_in_pdf(pdf, "_________________\n", 10, 10)

        # putting news in database
        if dict_of_args.get("date") is None:
            put_into_db(news_info.feed, news_info.title,
                        feed_entry.get("published_parsed", feed_entry.published_parsed),
                        news_info.description, news_info.link, news_info.link_of_img)
    try:
        pdf.output(filename)
        print("News were written in pdf file")

        for i in range(count):
            os.remove("img" + str(i) + ".jpg")
    except Exception:
        logging.error(Exception)
        print("Can't write information in pdf file")
