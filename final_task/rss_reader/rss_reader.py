import argparse
import xml.etree.ElementTree as ET
import requests
import json
import logging
import sys
from dataclasses import asdict
import jinja2.exceptions


import ClassNews
import CSVEntities
import ToPDF
import ToHTML


VERSION = 1.4


def args_parser(args):
    # Parse our arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', help="RSS URL")
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Date for selecting topics')
    parser.add_argument('--to-pdf', type=str, help='Convert news to pdf')
    parser.add_argument('--to-html', type=str, help='Convert news to html')

    res_args = parser.parse_args(args)
    return res_args


def get_dict_from_xml(rss_request, limit):
    main_title = ''
    root = ET.fromstring(rss_request.content)

    # Here we get title of api
    for channel_info in root.iter('channel'):
        for item in channel_info:
            if item.tag == 'title':
                main_title = item.text

    # Here we have the dictionary of articles
    res_dict_articles = ClassNews.xml_arguments_for_class(root, limit)
    return res_dict_articles, main_title


def get_request(args_source, timeout=None):
    logging.info('Start parsing')
    rss_request = requests.get(args_source, timeout=timeout)

    # Check status code
    status_code = rss_request.status_code
    logging.info("Status code {}".format(status_code))
    rss_request.raise_for_status()
    return rss_request


def articles_to_dict_articles(res_articles):
    dict_articles = []
    for article in res_articles:
        dict_articles.append(asdict(article))
    return dict_articles


def print_list(res_list):
    for article in res_list:
        print(article)


def convert_to_pdf(list_articles, path):
    ToPDF.print_article_list_to_pdf(list_articles, path)


def convert_to_html(list_articles, path):
    ToHTML.print_article_list_to_html(list_articles, path)


def convert_articles_to_json(res_dict_articles):
    json_articles = json.dumps(res_dict_articles, indent=4)
    return json_articles


def main():
    try:
        args = args_parser(sys.argv[1:])
        res_dict_articles = []
        logging_level = logging.CRITICAL
        if args.verbose:
            logging_level = logging.INFO

        if args.version:
            print("Current version: " + str(VERSION))
        if args.limit:
            print('News LIMIT: ' + str(args.limit))

        if args.source and (not args.date):
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

            # Get request
            rss_request = get_request(args.source)
            print(rss_request.status_code)
            logging.info('Parsing completed successfully')

            # Here we check the type of response. To correctly process it
            if rss_request.headers['content-type'] == "application/xml":

                res_dict_articles, main_title = get_dict_from_xml(rss_request, args.limit)

                logging.info('Print news:')

                print("\nFeed: {}".format(main_title))
                result_articles = ClassNews.dicts_to_articles(res_dict_articles)

                print_list(result_articles)

                res = CSVEntities.csv_to_python(result_articles, "datecsv.csv")
            else:
                logging.info(rss_request.headers['content-type'])
                logging.warning('We received not an xml file from api, sorry')

        if args.date:
            logging.info('Print news by date: ')
            result_articles = CSVEntities.return_news_to_date(args.date, "datecsv.csv", args.limit)
            res_dict_articles = articles_to_dict_articles(result_articles)
            if result_articles:
                if not (args.to_html or args.to_pdf):
                    print_list(result_articles)
            else:
                print("We don't have any news in cache %s" % args.date)

        if args.json and res_dict_articles:
            logging.info('Print result as JSON in stdout')
            print(convert_articles_to_json(res_dict_articles))
        if args.to_pdf:
            convert_to_pdf(result_articles, args.to_pdf)

        if args.to_html:
            convert_to_html(result_articles, args.to_html)

    except requests.exceptions.InvalidSchema:
        logging.critical('It is not http request!')
    except requests.exceptions.Timeout:
        logging.critical('Time to connect is out')
    except requests.exceptions.HTTPError as httpserr:
        logging.critical("Sorry, page not found")
    except requests.exceptions.InvalidURL:
        logging.critical("Sorry, that's not valid url")
    except requests.exceptions.ConnectionError:
        logging.critical("Sorry, you have an proxy or SSL error")
        # A proxy or SSL error occurred.
    except ToPDF.PisaError:
        logging.critical(ToPDF.PisaError.message)
    except FileNotFoundError:
        logging.critical("Sorry, path do not exist")
    except PermissionError:
        logging.critical("Sorry, you do not have access to this file.")
    except jinja2.exceptions.TemplateNotFound:
        logging.critical("Sorry, you forgot the template")


if __name__ == '__main__':
    main()