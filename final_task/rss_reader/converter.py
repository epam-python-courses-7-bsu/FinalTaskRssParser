from dominate.tags import div, h2, img, p, link
import dominate
import html

from . import news_parser, topdf


def createHtmlStructure(channel, limit, html_path, pdf_path):
    '''
    1. in loop create html structure
    2. return html_structure 
    3. or file name of pdf for send_from_directory function
    '''
    html_document = dominate.document(title="HTML document")

    for index, item in enumerate(channel.entries):
        if (index == limit):
            break
        with html_document:
            with div():
                h2("Title: " + html.unescape(item.title))
                p("Link: " + item.link)
                media_content = news_parser.checkMediaContent(item)
                if (media_content):
                    img(src=media_content)
                description = news_parser.getDescription(item.description)
                if (description):
                    p("Description: " + description)

    if (html_path):
        return str(html_document)
    elif(pdf_path):
        return topdf.convertHtmlToPdf(str(html_document), pdf_path)
