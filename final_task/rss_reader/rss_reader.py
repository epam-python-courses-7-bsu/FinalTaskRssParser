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


def get_dict_from_xml(rss_request, limit): #test
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
    rss_logging(logging, 'Start parsing', 'info')
    rss_request = requests.get(args_source, timeout=timeout)

    # Check status code
    status_code = rss_request.status_code
    rss_logging(logging, "Status code {}".format(status_code), 'info')
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
    if ToPDF.print_article_list_to_pdf(list_articles, path):
        rss_logging(logging, "News converted to pdf successfully", 'info')
    return True


def convert_to_html(list_articles, path):
    if ToHTML.print_article_list_to_html(list_articles, path):
        rss_logging(logging, "News converted to html successfully", 'info')
    return True


def convert_articles_to_json(res_dict_articles):
    json_articles = json.dumps(res_dict_articles, indent=4)
    return json_articles


def rss_logging(logger, msg, level):
    if level == 'critical':
        return logger.critical(msg)
    if level == 'info':
        return logger.info(msg)
    if level == 'warning':
        return logger.warning(msg)


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
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

        if args.source and (not args.date):
            # Get request
            rss_request = get_request(args.source)
            rss_logging(logging, 'Parsing completed successfully', 'info')
            rss_logging(logging, "Content type: %s" % rss_request.headers['content-type'], 'info')

            # Here we check the type of response. To correctly process it
            if rss_request.headers['content-type'] == "application/xml" or 'application/rss+xml':
                res_dict_articles, main_title = get_dict_from_xml(rss_request, args.limit)

                rss_logging(logging, 'Print news:', 'info')
                print("\nFeed: {}".format(main_title))
                result_articles = ClassNews.dicts_to_articles(res_dict_articles)
                print_list(result_articles)
                res = CSVEntities.csv_to_python(result_articles, "datecsv.csv")
            else:
                rss_logging(logging, rss_request.headers['content-type'], 'info')
                rss_logging(logging, 'We received not an xml file from api, sorry', 'warning')

        if args.date:
            rss_logging(logging, 'Search news by date: ', 'info')
            result_articles = CSVEntities.return_news_to_date(args.date, "datecsv.csv", args.limit)

            res_dict_articles = articles_to_dict_articles(result_articles)
            if result_articles:
                if not (args.to_html or args.to_pdf):
                    rss_logging(logging, 'Print news by date: ', 'info')
                    print_list(result_articles)
            else:
                rss_logging(logging, "We don't have any news in cache %s" % args.date, 'info')

        if args.json and res_dict_articles:
            rss_logging(logging, 'Print result as JSON in stdout', 'info')
            print(convert_articles_to_json(res_dict_articles))

        if args.to_pdf:
            convert_to_pdf(result_articles, args.to_pdf)

        if args.to_html:
            convert_to_html(result_articles, args.to_html)

    except requests.exceptions.InvalidSchema:
        rss_logging(logging, 'It is not http request!', 'critical')
    except requests.exceptions.Timeout:
        rss_logging(logging, 'Time to connect is out', 'critical')
    except requests.exceptions.HTTPError as httpserr:
        rss_logging(logging, 'Time to connect is out', 'critical')
    except requests.exceptions.InvalidURL:
        rss_logging(logging, "Sorry, that's not valid url", 'critical')
    except requests.exceptions.ConnectionError:
        rss_logging(logging, 'Sorry, you have an proxy or SSL error', 'critical')
        # A proxy or SSL error occurred.
    except FileNotFoundError:
        rss_logging(logging, "Sorry, path do not exist", 'critical')
    except PermissionError:
        rss_logging(logging, "Sorry, you do not have access to this file.", 'critical')
    except jinja2.exceptions.TemplateNotFound:
        rss_logging(logging, "Sorry, you forgot the template", 'critical')


if __name__ == '__main__':
    main()