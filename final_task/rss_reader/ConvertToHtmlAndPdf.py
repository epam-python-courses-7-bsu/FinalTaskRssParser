import os
import sys
from fpdf import FPDF
from News import News
from dominate.tags import html, head, meta, body, div, img, p, b, br, h1, a

from WorkWithCache import correct_title
from Log import log_decore
from RssException import RssException

@log_decore
def convert_Dict_to_News(arr_news_dict):
    all_news = []
    for item_news in arr_news_dict:
        tmp_img_link = item_news["links"]
        tmp_link = item_news["link"]
        tmp_news = item_news["news"]
        tmp_title = item_news["title"]
        tmp_date = item_news["date"]
        tmp_date_str_date = item_news["strDate"]
        item_of_list_news = News(tmp_news, tmp_link, tmp_title, tmp_date, tmp_img_link, tmp_date_str_date)
        all_news.append(item_of_list_news)
    return all_news



'''create an HTML file and fill it with news'''
@log_decore
def create_html_news(path, News):
    if os.path.isdir(path) is False:
        raise RssException("Error. It isn't a folder")

    path = os.path.join(path, "News.html")

    news_html = html()
    news_html.add(head(meta(charset='utf-8')))
    news_body = news_html.add(body())
    with news_body:
        for item_news in News:
            news_body = news_body.add(div())
            news_body += h1(item_news.title)
            news_body += p(b("Date: "), a(item_news.date))

            text = item_news.news

            # remove links in the text and add pictures
            if len(item_news.links) > 0:
                start = text.find(']', 0, len(text))
                text = text[start + 1:]

                this_dir = os.path.abspath(os.path.dirname(__file__))
                sys.path.append(this_dir)
                news_body += img(src=f"file:///{this_dir}/images/{correct_title(item_news.title)}.jpg")
            else:
                # if there are no pictures, just remove the links
                start = text.find(']', 0, len(text))
                text = text[start + 1:]

            news_body += p(text.encode("utf-8").decode("utf-8"), br(), br())

    try:
        with open(path, 'w', encoding='utf-8') as rss_html:
            rss_html.write(str(news_html))
    except FileNotFoundError:
        raise RssException('Error. No such folder\n')
    print("file News.html created")



'''create an PDF file and fill it with news'''
@log_decore
def create_pdf_news(path, News):
    if os.path.isdir(path) is False:
        raise RssException("Error. It isn't a folder")
    path = os.path.join(path, "News.pdf")

    pdf = FPDF()
    try:
        pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font("DejaVuSans")
    except RuntimeError:
        raise RssException("fonts file not found")
    pdf.alias_nb_pages()
    pdf.add_page()

    for item_news in News:
        text = item_news.news
        # remove links in the text and add pictures

        start = text.find(']', 0, len(text))
        text = text[start + 1:]

        pdf.set_font_size(26)
        pdf.write(11, item_news.title + '\n\n')
        pdf.set_font_size(14)
        pdf.write(11, f"Date: {item_news.date}\n")

        this_dir = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(this_dir)
        if len(item_news.links) > 0:
            try:
                pdf.image(f'{this_dir}/images/{correct_title(item_news.title)}.jpg', w=75, h=75)
            except RuntimeError:
                pass
        pdf.write(10, "\n")
        pdf.write(10, text + "\n\n\n\n")
    pdf.output(path, 'F')
    try:
        pdf.output(path, 'F')
    except FileNotFoundError:
        raise RssException("Error. No such folder")
    print("file News.pdf created")
