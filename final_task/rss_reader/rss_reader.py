import argparse
import logging
import parser_rss
import exceptions
import news_converter
import tools
from item_group import get_item_group_from_feedparser
from log import turn_on_logging
from news_storage import save_news, get_news_by_date
from datetime import datetime
from colorama import init as init_color


STORAGE_FILE = 'news.data'
VERSION = '5.0'


def create_arg_parser():
    """ Create and return argument parser.

    :return: argument parser
    :rtype: 'argparse.ArgumentParser'
    """
    arg_parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')

    arg_parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    arg_parser.add_argument('--version', action='version', help='Print version info', version='%(prog)s v' + VERSION)
    arg_parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    arg_parser.add_argument('--verbose', action='store_true', help='Output verbose status messages')
    arg_parser.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')
    arg_parser.add_argument('--date', type=lambda d: datetime.strptime(d, '%Y%m%d'),
                            help='News from the specified day will be printed out. Format: YYYYMMDD')
    arg_parser.add_argument('--to-pdf', type=str, help='Create PDF file with news', metavar='PATH')
    arg_parser.add_argument('--to-html', type=str, help='Create HTML file with news', metavar='PATH')
    arg_parser.add_argument('--colorize', action='store_true', help='Print news in colorized mode (not for json mode)')

    return arg_parser


def print_news(json_arg, item_group):
    """ Print news in stdout

    :param json_arg: if True news print as json
    :type json_arg: bool
    :type item_group: 'item_group.ItemGroup'
    """
    if json_arg:
        logging.info('Converting item group to json string.')
        json_str = news_converter.news_as_json_str(item_group)

        logging.info('Printing news as json.')
        print(json_str)
    else:
        logging.info('Printing news.')
        print(item_group)


def print_news_from_list(json_arg, news):
    """ Print news in stdout

    :param json_arg: if True news print as json
    :type json_arg: bool
    :type news: list of 'item_group.ItemGroup'
    """
    if json_arg:
        logging.info('Converting list of item group to json string.')
        json_str = news_converter.news_as_json_str_from_list(news)

        logging.info('Printing news as json.')
        print(json_str)
    else:
        for news_group in news:
            print_news(json_arg, news_group)
            print('-------------------------------------------------------------------------------------\n')


def write_in_file(html_path, pdf_path, item_groups):
    """ Write news as HTML or/and PDF in file

    :param html_path: path to HTML file for writing
    :type html_path: str
    :param pdf_path: path to PDF file for writing
    :type pdf_path: str

    :param item_groups: news for writing
    :type item_groups: list of 'item_group.ItemGroup'
    """
    if html_path:
        if not html_path.endswith('.html'):
            html_path += '.html'

        logging.info('Getting HTML code.')
        html_code = news_converter.news2html(item_groups)

        logging.info('Writing news in ' + html_path)
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_code)

    if pdf_path:
        if not pdf_path.endswith('.pdf'):
            pdf_path += '.pdf'

        logging.info('Writing news in ' + pdf_path)
        news_converter.news2pdf(item_groups, pdf_path)


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    if args.verbose:
        logging.info('Turning on logging.')
        turn_on_logging(logging.getLogger())

    if not args.source and not args.date:
        logging.error('Source or/and date must be specified.')
        arg_parser.print_help()
    elif not args.limit or args.limit > 0:
        tools.colorize = args.colorize
        init_color()

        if args.date:
            work_with_local_storage(args)
        else:
            work_with_internet(args)
    else:
        logging.error('Incorrect limit value!')


def work_with_local_storage(args):
    try:
        logging.info('Getting news by date ' + str(args.date) + ' from storage ' + STORAGE_FILE)
        news_by_date = get_news_by_date(args.date, STORAGE_FILE, args.source, args.limit)
    except exceptions.StorageNotFoundError as exc:
        logging.error(exc)
    except exceptions.NewsNotFoundError as err:
        logging.error(err)
    else:
        if args.to_html or args.to_pdf:
            write_in_file(args.to_html, args.to_pdf, news_by_date)
        else:
            print_news_from_list(args.json, news_by_date)


def work_with_internet(args):
    try:
        logging.info('Creating feedparser.')
        rss_feedparser = parser_rss.create_feedparser(args.source, args.limit)

        logging.info('Getting item group.')
        item_group = get_item_group_from_feedparser(rss_feedparser)

    except exceptions.GettingRSSException as exc:
        logging.error(exc)
    else:
        logging.info('Saving news in ' + STORAGE_FILE)
        save_news(args.source, item_group, STORAGE_FILE)

        if args.to_html or args.to_pdf:
            lst = list()
            lst.append(item_group)

            write_in_file(args.to_html, args.to_pdf, lst)
        else:
            print_news(args.json, item_group)


if __name__ == '__main__':
    main()
