import os
from fpdf import FPDF

FILENAME_PDF = "articles.pdf"


def conv_str(input_str):
    return (input_str.replace('\u2026', '').replace('\u2019', '').replace('\u201c', '').replace('\u201d', '')\
        .replace('\u2013', '').replace('\u2018', ''))


class PDF(FPDF):

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def print_article_list_to_pdf(list_articles, path):

    if not os.path.exists(path):
             raise FileNotFoundError
    path = os.path.join(path, FILENAME_PDF)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    for item in list_articles:
        pdf.cell(0, 10, "Title: %s" % (conv_str(item.title)), 0, 1)
        pdf.cell(0, 10, "Date: %s" % (conv_str(item.date)), 0, 1)
        pdf.cell(0, 10, "Link: %s" % (conv_str(item.link)), 0, 1)
        pdf.multi_cell(0, 10, '%s' % (conv_str(item.article)), 0, 1)
        for idx, link in enumerate(item.links):
            pdf.multi_cell(0, 10, "[%d]:%s" % (idx, (conv_str(link))), 0, 1)
        pdf.cell(0, 10, "", 0, 1)
    pdf.output(path, 'F')
    return True