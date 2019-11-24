from xhtml2pdf import pisa
import os

import ToHTML

FILENAME_PDF = "articles.pdf"


class PisaError(Exception):
    def __init__(self, msg):
        self.message = msg


def print_article_list_to_pdf(list_articles, path):
    if not os.path.exists(path):
        raise FileNotFoundError

    with open(os.path.join(path, FILENAME_PDF), "wb") as pdf:
        list_articles
        pisa_pdf = pisa.CreatePDF(ToHTML.print_article_list(list_articles), dest=pdf)
        if not pisa_pdf.err:
            print('Please, check %s' % path)
        else:
            raise PisaError("Sorry, you have problem with converting to pdf")