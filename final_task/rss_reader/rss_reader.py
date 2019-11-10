import argparse
import re
import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime

import RssReaderExceptions as rre
import ClassNews

VERSION = 1.1

# Parse our arguments
parser = argparse.ArgumentParser()
parser.add_argument("sourse", help="RSS URL")
parser.add_argument('--version', action='store_true', help='Print version info')
parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

args = parser.parse_args()

if args.version:
    print("Current version: " + str(VERSION))
if args.limit:
    print('News LIMIT: ' + str(args.limit))


def log(message):
    """Here we are print a log message"""
    if args.verbose:
        print('\n' + message + '\n')


try:
    # Check if the request is valid
    # if not re.match("(https|http):\/\/((\w+).)+(com|org|ru|net)(\/(\w+))+", args.sourse):
    #     raise rre.NotRequest

    # Get request
    log('Start parsing')
    rss_request = requests.get(args.sourse)

    # to check ReadTimeout exception
    # rss_request = requests.get(args.sourse, timeout=(1, 0.01))

    # Check status code
    status_code = rss_request.status_code
    log("Status code {}".format(status_code))
    # if status_code == 404:
    #     raise requests.exceptions.HTTPError
    rss_request.raise_for_status()

    log('Parsing completed successfully')

    # Here we check the type of response. To correctly process it
    if rss_request.headers['content-type'] == "application/xml":
        root = ET.fromstring(rss_request.content)

        # Here we get title of api
        for child in root.iter('channel'):
            for item in child:
                if item.tag == 'title':
                    main_title = item.text

        # Here we have the dictionary of articles
        my_dict_articles = ClassNews.xml_arguments_for_class(root, args.limit)
        # print(my_dict_articles)

        log('Print news:')
        print("\nFeed: {}".format(main_title))
        my_articles = ClassNews.dicts_to_articles(my_dict_articles)
        for article in my_articles:
            print(article)
    else:
        log(rss_request.headers['content-type'])
        log('We received not an xml file from api, sorry')
    if args.json:
        log('Print result as JSON in stdout')
        json_articles = json.dumps(my_dict_articles, indent=4)
        log(json_articles)
# except rre.NotRequest as exc:
#     log(str(exc))
except requests.exceptions.MissingSchema:
    log('it is not http request!')
except requests.exceptions.ConnectTimeout:
    log('Time to connect is out')
except requests.exceptions.ReadTimeout:
    log('Time to read is out')
except requests.exceptions.HTTPError as httpserr:
    log("Sorry, page not found")
except requests.exceptions.InvalidURL:
    log("Sorry, that's not valid url")
except requests.exceptions.ConnectionError:
    log("Sorry, you have an proxy or SSL error")
    # A proxy or SSL error occurred.
