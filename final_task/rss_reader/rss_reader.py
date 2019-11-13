import logging
import os
import sys

directory_to_module = os.path.abspath(os.path.dirname(__file__))
sys.path.append(directory_to_module)

import articles_handler
import argparse_handler
import custom_error

LOG_FILE_NAME = directory_to_module + '\\app.log'


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

            if args.json:
                print(articles_handler.create_rss_json(articles_list))
                logging.info('Articles was printed as json')
            else:
                articles_handler.print_rss_articles(articles_list)
                logging.info(f'{len(articles_list)} articles was printed')

            logging.info('Application ended')
        elif switcher == 'date_only':
            arg_parser = argparse_handler.create_parser('no link')
            logging.info('Argument parser created')

            args = arg_parser.parse_args()

            limit = args.limit

            cache_handler = articles_handler.CachedArticlesClass()
            cache_handler.get_articles_from_cache()

            articles_on_date_list = cache_handler.make_list_of_articles_by_date_and_url(args.date, None, limit)

            if args.json:
                print(articles_handler.create_rss_json(articles_on_date_list))
                logging.info('Articles was printed as json')
            else:
                articles_handler.print_rss_articles(articles_on_date_list)
                logging.info(f'{len(articles_on_date_list)} articles was printed')

            logging.info('Application ended')
        elif switcher == 'link_and_date':
            arg_parser = argparse_handler.create_parser('full')
            logging.info('Argument parser created')

            args = arg_parser.parse_args()

            rss_url = args.source
            limit = args.limit

            cache_handler = articles_handler.CachedArticlesClass()
            cache_handler.get_articles_from_cache()

            articles_on_date_list = cache_handler.make_list_of_articles_by_date_and_url(args.date, rss_url, limit)

            if args.json:
                print(articles_handler.create_rss_json(articles_on_date_list))
                logging.info('Articles was printed as json')
            else:
                articles_handler.print_rss_articles(articles_on_date_list)
                logging.info(f'{len(articles_on_date_list)} articles was printed')

            logging.info('Application ended')
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
        print('No data in cache file')


if __name__ == '__main__':
    main()
