#!/usr/bin/env python3.8

import dominate
import dominate.tags as tag

from utils import create_path_to_file

from rss_exceptions import PATHError


def convert_news_to_html(cmd_args, all_news, logger):
    """
    If the 'to-html' argument was passed - creates HTML file and push data in it.
    """
    if cmd_args.to_html:
        logger.info("Call function for creation HTML file")
        create_html_file(cmd_args, all_news, logger)


def create_html_file(cmd_args, all_news, logger):
    """
    Creates and fills in the HTML file with the required data
    """
    path_to_html = create_path_to_file(cmd_args.to_html, 'RSS_NEWS.html', logger)

    rss_html_doc = dominate.document(title='RSS NEWS')

    with rss_html_doc:
        tag.h1("RSS News")

    for num, new in enumerate(all_news, 1):
        logger.info(f'Add new № {num} in HTML file.')
        rss_html_doc = convert_new_in_html(cmd_args, new, rss_html_doc)

    try:
        logger.info('Create HTML file in the specified directory.')

        with open(path_to_html, 'w') as file:
            file.write(str(rss_html_doc))

        logger.info("HTML file was created and filled in successfully")

    except FileNotFoundError:
        raise PATHError('Setted PATH is invalid')


def convert_new_in_html(cmd_args, new, html_file):
    """
    Convert one new to HTML format
    """

    with html_file:
        with tag.div():
            tag.h2(new.get('title'))
            tag.p(new.get('date'))
            tag.br()
            tag.a("Read the full article", href=new.get('link'))
            tag.br()
            tag.br()

            if cmd_args.date:
                for num, link in enumerate(new.get('img_link'), 1):
                    tag.a(f"Image link № {num}", href=link)
                    tag.br()
            else:
                for num, link in enumerate(new.get('img_link')):
                    tag.img(src=link, alt=new.get('img_title')[num])
                    tag.br()

            tag.p(new.get('text'))
            tag.br()

    return html_file
