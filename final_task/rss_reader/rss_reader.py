import argparse
import xml.etree.ElementTree as ET
import requests
import json
import logging

import rss_reader.ClassNews as ClassNews

VERSION = 1.1


def arg_parser():
    # Parse our arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs='?', help="RSS URL")
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()
    return args


def main():
    try:
        args = arg_parser()
        logging_level = logging.CRITICAL
        if args.verbose:
            logging_level = logging.INFO
        if args.version:
            print("Current version: " + str(VERSION))
        if args.limit:
            print('News LIMIT: ' + str(args.limit))

        res_dict_articles = []

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
        if args.source:
            # Get request
            logging.info('Start parsing')
            rss_request = requests.get(args.source)

            # Check status code
            status_code = rss_request.status_code
            logging.info("Status code {}".format(status_code))

            rss_request.raise_for_status()

            logging.info('Parsing completed successfully')

            # Here we check the type of response. To correctly process it
            if rss_request.headers['content-type'] == "application/xml":
                root = ET.fromstring(rss_request.content)

                # Here we get title of api
                for channel_info in root.iter('channel'):
                    for item in channel_info:
                        if item.tag == 'title':
                            main_title = item.text

                # Here we have the dictionary of articles
                res_dict_articles = ClassNews.xml_arguments_for_class(root, args.limit)

                logging.info('Print news:')
                if main_title:
                    print("\nFeed: {}".format(main_title))
                result_articles = ClassNews.dicts_to_articles(res_dict_articles)

                for article in result_articles:
                    print(article)
            else:
                logging.info(rss_request.headers['content-type'])
                logging.warning('We received not an xml file from api, sorry')

        if args.json and res_dict_articles:
            logging.info('Print result as JSON in stdout')
            json_articles = json.dumps(res_dict_articles, indent=4)
            print(json_articles)

    except requests.exceptions.InvalidSchema:
        logging.critical('It is not http request!')
    except requests.exceptions.ConnectTimeout:
        logging.critical('Time to connect is out')
    except requests.exceptions.ReadTimeout:
        logging.critical('Time to read is out')
    except requests.exceptions.HTTPError as httpserr:
        logging.critical("Sorry, page not found")
    except requests.exceptions.InvalidURL:
        logging.critical("Sorry, that's not valid url")
    except requests.exceptions.ConnectionError:
        logging.critical("Sorry, you have an proxy or SSL error")
        # A proxy or SSL error occurred.


if __name__ == '__main__':
    main()