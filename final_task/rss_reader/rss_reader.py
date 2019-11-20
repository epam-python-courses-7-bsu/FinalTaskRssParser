import argparse
import re
from termcolor import colored
import os
import colorama
from database_functions import *
from parse_rss_functions import get_news_list
from personal_exceptions import *
from print_functions import *
from save_in_format_functions import save_in_fb2, save_in_html

VERSION = 4


def main():
    """
    The main entry point of the application
    """
    colorama.init()
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    argument_parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
    argument_parser.add_argument('--version', action='store_true', help='print version info')
    argument_parser.add_argument('--limit', help='limit news topics if this parameter provided')
    argument_parser.add_argument('--date', help='represent news from local storage by date')
    argument_parser.add_argument('--to-html', help='save news in html format')
    argument_parser.add_argument('--to-fb2', help='save news in fb2 format')
    argument_parser.add_argument('source')
    arguments = argument_parser.parse_args()
    if arguments.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename='sample.log', filemode='w', level=logging.INFO)
    logging.info('Program started')
    if arguments.to_html:
        if not os.path.exists(arguments.to_html):
            logging.error('Inrorrect html filepath')
            raise IncorrectFilePath('Inrorrect html filepath')
    if arguments.to_fb2:
        if not os.path.exists(arguments.to_html):
            logging.error('Inrorrect fb2 filepath')
            raise IncorrectFilePath('Inrorrect fb2 filepath')
    if arguments.limit:
        if not re.match('\\d+', arguments.limit):
            logging.error('Input value of --limit is incorrect')
            raise ValueError('Input value of --limit is incorrect')
        arguments.limit = int(arguments.limit)
    if arguments.date:
        if not re.match('\\d+', arguments.date) or len(arguments.date) != 8:
            logging.error('Input value of --date is incorrect')
            raise ValueError('Input value of --date is incorrect')
        news_list = get_news_list_by_date(arguments.date, arguments.limit)
        if arguments.to_html or arguments.to_fb2:
            if arguments.to_html:
                save_in_html(arguments.to_html, news_list)
            if arguments.to_fb2:
                save_in_fb2(arguments.to_fb2, news_list)
        else:
            if news_list:
                if arguments.json:
                    print_news_JSON(news_list)
                else:
                    print_news(news_list)
            else:
                print('No news by this date')
        return
    if arguments.version:
        print(f'Program version - {VERSION}')
    news_list = get_news_list(arguments.source, arguments.limit)
    if arguments.to_html or arguments.to_fb2:
        if arguments.to_html:
            save_in_html(arguments.to_html, news_list)
        if arguments.to_fb2:
            save_in_fb2(arguments.to_fb2, news_list)
    else:
        if arguments.json:
            print_news_JSON(news_list)
        else:
            print_news(news_list)
    write_news_to_database(news_list)


if __name__ == '__main__':
    try:
        main()
    except IncorrectURL as e:
        print(colored(e, 'red'))
        logging.error(e)
    except NoInternet as e:
        print(colored(e, 'red'))
        logging.error(e)
    except ValueError as e:
        print(colored(e, 'red'))
        logging.error(e)
    except IncorrectFilePath as e:
        print(colored(e, 'red'))
        logging.error(e)
    finally:
        logging.info('Program ended')
