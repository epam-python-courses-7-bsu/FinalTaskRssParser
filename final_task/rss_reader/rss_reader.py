import argparse
import json
import logging
from urllib import request, error
from parser import xml_parser


def go_for_rss(url):
    """getting data"""
    try:
        response = request.urlopen(url)
    except error.HTTPError as ex:
        logging.info(ex)
        raise
    return response


def output_format(news_articles, json_output=False):
    """formating data to the format we choose. default='str'"""
    logging.info('Formating output')
    # return json if we asked for it
    if json_output:
        for article in news_articles:
            result = json.dumps(article.__dict__, ensure_ascii=False, indent=4)
            yield result
    # if not, return data as string
    else:
        for article in news_articles:
            yield article


def print_result(result, limit):
    if limit:
        limit = int(limit)
        for article in result:
            if limit > 0:
                print(article)
                limit -= 1
    else:
        for article in result:
            print(article)


def get_args():
    parser = argparse.ArgumentParser(description="Pure python command-line RSS reader")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="version", version='rss_reader 0.2.0')
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    return parser.parse_args()


def main():
    args = get_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    logging.info(f'Started getting data from {args.source}')
    try:
        response = go_for_rss(args.source)
    except Exception as ex:
        logging.info(ex)
        print('Website is not working or Url is not correct. Please, restart the program with a correct url')
        return None
    logging.info(f'Data recieved from {args.source}')

    logging.info('Parsing XML data')

    news_articles = xml_parser(response, args.limit)
    logging.info('Parsing is finished')

    logging.info('Preparing output')
    result = output_format(news_articles, args.json)

    logging.info('Printing result')
    print_result(result, args.limit)


if __name__ == "__main__":
    main()
