import argparse
import re
from termcolor import colored
import os
import colorama
import logging
from database_functions import get_news_list_by_date, write_news_to_database
from parse_rss_functions import get_news_list
from custom_exceptions import NoInternet, IncorrectURL, IncorrectFilePath, DatabaseConnectionError
from print_functions import print_news_colorize, print_news_JSON_colorize, print_news, print_news_JSON
from save_in_format_functions import save_in_fb2, save_in_html
from arguments_functions import check_date_argument, check_fb2_argument, check_html_argument, \
    check_limit_argument, get_arguments

VERSION = 5


def main():
    """
    The main entry point of the application
    """
    colorama.init()
    arguments = get_arguments()
    if arguments.version:
        print(f'Program version - {VERSION}')
        return
    if arguments.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename='sample.log', filemode='w', level=logging.INFO)
    logging.info('Program started')
    if arguments.to_html:
        check_html_argument(arguments.to_html)
    if arguments.to_fb2:
        check_fb2_argument(arguments.to_fb2)
    if arguments.limit:
        check_limit_argument(arguments.limit)
        arguments.limit = int(arguments.limit)
    if arguments.date:
        check_date_argument(arguments.date)
        news_list = get_news_list_by_date(arguments.date, arguments.limit)
        if arguments.to_html or arguments.to_fb2:
            if arguments.to_html:
                save_in_html(arguments.to_html, news_list, f"news_by_date-{arguments.date}.html")
            if arguments.to_fb2:
                save_in_fb2(arguments.to_fb2, news_list, f"news_by_date-{arguments.date}.fb2")
        else:
            if news_list:
                if arguments.colorize:
                    if arguments.json:
                        print_news_JSON_colorize(news_list)
                    else:
                        print_news_colorize(news_list)
                else:
                    if arguments.json:
                        print_news_JSON(news_list)
                    else:
                        print_news(news_list)
            else:
                print('No news by this date')
        return
    news_list = get_news_list(arguments.source, arguments.limit)
    if arguments.to_html or arguments.to_fb2:
        if arguments.to_html:
            save_in_html(arguments.to_html, news_list, f"news_from-{arguments.source[8:-4]}.html")
        if arguments.to_fb2:
            save_in_fb2(arguments.to_fb2, news_list, f"news_from-{arguments.source[8:-4]}.fb2")
    else:
        if arguments.colorize:
            if arguments.json:
                print_news_JSON_colorize(news_list)
            else:
                print_news_colorize(news_list)
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
    except DatabaseConnectionError as e:
        print(colored(e, 'red'))
        logging.error(e)
    finally:
        logging.info('Program ended')
