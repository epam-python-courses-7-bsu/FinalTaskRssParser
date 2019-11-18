import logging
import os
import sys
from typing import List

directory_to_module = os.path.abspath(os.path.dirname(__file__))
sys.path.append(directory_to_module)

import single_article
import html_converter
import pdf_converter
import articles_handler
import argparse_handler
import custom_error

LOG_FILE_NAME = os.path.join(directory_to_module, 'app.log')


def start_logging() -> None:
    """Setting up logging basic configuration"""
    root = logging.getLogger()
    logging.basicConfig(
        filename=LOG_FILE_NAME,
        filemode='w',
        format='[%(asctime)s] %(levelname)-8s %(message)s',
        level=logging.DEBUG
    )
    if "--verbose" in sys.argv:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)


def converting_starter(key: str, list_with_articles: List[single_article.SingleArticle], path_to_file: str) -> None:
    """Starts the chosen conversion"""
    logging.info(f"Converting to {key} started")
    if key == 'html':
        html_converter.convert_to_html(list_with_articles, path_to_file)
    else:
        pdf_converter.convert_to_pdf(list_with_articles, path_to_file)
    logging.info(f"Converting to {key} ended")


def arguments_logic(args, list_of_articles):
    conversion = False

    if args.to_html:
        conversion = True
        converting_starter('html', list_of_articles, args.to_html)
    if args.to_pdf:
        conversion = True
        converting_starter('pdf', list_of_articles, args.to_pdf)

    if not conversion:
        if args.json:
            print(articles_handler.create_rss_json(list_of_articles))
            logging.info('Articles was printed as json')
        else:
            articles_handler.print_rss_articles(list_of_articles)
            logging.info(f'{len(list_of_articles)} articles was printed')

    logging.info('Application ended')


def main() -> None:
    """The main entry point of the application"""
    try:
        start_logging()
        logging.info('Application started')

        argparse_handler.check_the_arguments_amount()
        switcher = argparse_handler.check_if_url_or_date_in_arguments()

        if switcher == 'help':
            arg_parser = argparse_handler.create_parser('full')
            logging.info('Argument parser created')

            logging.info('Help was printed')
            logging.info('Application ended')

            arg_parser.parse_args()
        elif switcher == 'version':
            arg_parser = argparse_handler.create_parser('full')
            logging.info('Argument parser created')

            logging.info('Version was printed')
            logging.info('Application ended')

            arg_parser.parse_args()
        elif switcher == 'link_only':
            arg_parser = argparse_handler.create_parser('full')
            logging.info('Argument parser created')

            args = arg_parser.parse_args()

            rss_url = args.source
            limit = args.limit

            parsed_rss = articles_handler.parse_rss(rss_url)
            logging.info('RSS URL parsed')

            articles_list = articles_handler.get_articles(parsed_rss, limit)
            logging.info('Articles list created')

            cache_handler = articles_handler.CachedArticlesClass()
            cache_handler.save_articles_to_cache(articles_list)

            arguments_logic(args, articles_list)
        elif switcher == 'date_only':
            arg_parser = argparse_handler.create_parser('no link')
            logging.info('Argument parser created')

            args = arg_parser.parse_args()

            limit = args.limit

            cache_handler = articles_handler.CachedArticlesClass()
            cache_handler.get_articles_from_cache()

            articles_on_date_list = cache_handler.make_list_of_articles_by_date_and_url(args.date, None, limit)

            arguments_logic(args, articles_on_date_list)
        elif switcher == 'link_and_date':
            arg_parser = argparse_handler.create_parser('link_and_date')
            logging.info('Argument parser created')

            args = arg_parser.parse_args()

            rss_url = args.source
            limit = args.limit

            cache_handler = articles_handler.CachedArticlesClass()
            cache_handler.get_articles_from_cache()

            articles_on_date_list = cache_handler.make_list_of_articles_by_date_and_url(args.date, rss_url, limit)

            arguments_logic(args, articles_on_date_list)
    except custom_error.UrlNotFoundInArgsError:
        logging.error('UrlNotFoundInArgsError')
        logging.info('Application ended')
        print("Url is not found in the arguments")
    except custom_error.NotEnoughArgumentsError:
        logging.error('Not enough arguments(URL link is required)')
        logging.info('Application ended')
        print("Not enough arguments(URL link is required)")
    except custom_error.NotValidUrlError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print(error.message)
    except custom_error.ConnectionFailedError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print('Connection failed')
    except custom_error.ArticleKeyError as error:
        logging.error(error.message)
        logging.info('Application ended')
    except custom_error.NotValidDateError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print(error.message)
    except custom_error.NotValidLimitError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print(error.message)
    except custom_error.NoDataInCacheFileError:
        logging.error('No data in cache file')
        logging.info('Application ended')
        print('No data in cache file')
    except custom_error.NotValidPathError as error:
        logging.error(error.message)
        logging.info('Application ended')
        print(error.message)


if __name__ == '__main__':
    main()
