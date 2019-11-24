from xhtml2pdf import pisa
import ToHTML

def print_article_list_to_pdf(list_articles, file_name):
    with open(file_name, "wb") as pdf:
        list_articles
        pisa_pdf = pisa.CreatePDF(ToHTML.print_article_list(list_articles), dest=pdf)
        if not pisa_pdf.err:
            print('Please, check %s' % file_name)