import os
import json
import urllib
from colored import attr, fg, bg
from ebooklib import epub
from fpdf import FPDF


def get_output_function(converter):
    """Output factory"""
    if converter == 'json':
        return output_json
    elif converter == 'pdf':
        return output_pdf
    elif converter == 'epub':
        return output_epub
    elif converter == 'color':
        return colored_output
    elif converter == 'text':
        return output


def colored_output(logger, all_news, about_website=None, file_name=None):
    """Function which print information about site  and a set of news with multi-colored text."""
    logger.info('Output multi-colored news =)')
    red = fg(1)
    black = fg(0)
    green = fg(28)
    blue = fg(21)
    purple = fg(55)
    background_site = bg(225)
    background_news = bg(195)
    reset = attr(0)
    if about_website is not None:
        for key, value in about_website.items():
            print(f'{background_site}\n{red}{key}: {purple}{value}{reset}')
    for number_of_news in all_news:
        print(f"{background_news}{black}--------------------------------------------------------{reset}")
        for key, value in number_of_news.items():
            print(f'{background_news}{green}{key}: {blue}{value}{reset}')


def output(logger, all_news, about_website=None, file_name=None):
    """Function which print information about site and a set of news."""
    logger.info('Output news')
    if about_website is not None:
        for key, value in about_website.items():
            print(f'\n{key}: {value}')
    for number_of_news in all_news:
        print("--------------------------------------------------------")
        for key, value in number_of_news.items():
            print(f'{key}: {value}')


def parse_to_json(dictionary):
    return json.dumps(dictionary, indent=4)


def output_json(logger, all_news, about_website=None, file_name=None):
    """Function which print news in stdout in json-format."""
    if about_website is not None:
        logger.info('Convert to JSON-format')
        print(parse_to_json([about_website] + all_news))
    else:
        logger.info('Convert news to JSON-format fom cache')
        print(parse_to_json(all_news))


def output_pdf(logger, all_news, about_website=None, file_name=None):
    """Function which create or overwrites PDF-file with selected fresh or cached news"""
    logger.info('Convert to PDF-format')
    pdf = FPDF()
    pdf.add_page()
    if about_website is not None:
        pdf.set_font("Arial", "B", size=14)
        pdf.set_fill_color(200, 220, 255)
        for value in about_website.values():
            line = 1
            pdf.cell(190, 8, txt=value, ln=line, align="C")
            line += 1
    pdf.set_font("Arial", size=10)
    pdf.set_line_width(1)
    pdf.set_draw_color(35, 41, 153)
    for news in all_news:
        link = news['Source of image']
        for key, value in news.items():
            if key != 'Summary':
                pdf.multi_cell(190, 6, txt=f'{key}: {value}', align="L")
            else:
                position_y = pdf.get_y()
                try:
                    filename, _ = urllib.request.urlretrieve(link)
                    pdf.image(filename, 80, position_y, h=30, type='jpeg', link=link)
                    pdf.ln(31)
                    os.remove(filename)
                except Exception as ex:
                    logger.warning("Error finding image: {}, {}.".format(type(ex), ex))
                pdf.multi_cell(190, 6, txt=f'{key}: {value}', align="L")
        position_y = pdf.get_y()
        pdf.set_line_width(1)
        pdf.set_draw_color(35, 41, 153)
        pdf.line(10, position_y, 200, position_y)
    logger.info('Creating of PDF-file')
    try:
        pdf.output(file_name)
        logger.info('Converted successfully!')
    except Exception as ex:
        logger.error("PDF file writing error : {}, {}.".format(type(ex), ex))


def output_epub(logger, all_news, about_website=None, file_name=None):
    """Function which create or overwrites EPUB-file with selected fresh or cached news"""
    logger.info('Convert to EPUB-format')
    book = epub.EpubBook()
    if about_website is not None:
        book.set_title(f'RSS news from {about_website["Feed"]}')
    else:
        book.set_title('RSS news')
    book.set_language('en')
    chapters = []
    for news in all_news:
        chapter = epub.EpubHtml(title=f'Chapter of {news["Date"]}', file_name=f'chap {news["Title"]}.xhtml')
        title = f'<h1>{news["Title"]}</h1>'
        if news["Source of image"] == "No image":
            image = ''
        else:
            image = f'<img src="{news["Source of image"]}">'
        string_of_epub_content = f'Date: {news["Date"]}<br/>'
        string_of_epub_content += f'Link: {news["Link"]}<br/>'
        string_of_epub_content += f'Summary: {news["Summary"]}<br/>'
        string_of_epub_content += f'Source of image: {news["Source of image"]}<br/>'
        chapter.content = f'{title}{image}<p align="left">{string_of_epub_content}</p>'
        book.add_item(chapter)
        chapters.append(chapter)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = chapters
    logger.info('Creating of PDF-file')
    try:
        epub.write_epub(file_name, book, {})
        logger.info('Converted successfully!')
    except Exception as ex:
        logger.error("Error finding image: {}, {}.".format(type(ex), ex))
