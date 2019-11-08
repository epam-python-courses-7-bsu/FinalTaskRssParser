import feedparser
import sys
import datetime
import argparse
import json
from bs4 import BeautifulSoup

DEFAULT_LIMIT_COUNT = 3
VERSION = '1.0'


class RSSReader:
    is_verbose = False  # logging is disabled by default
    is_json = False
    limit = DEFAULT_LIMIT_COUNT

    def __init__(self, url):
        self.url = url

    def url_parsing(self):
        parsed_url = feedparser.parse(self.url)
        if parsed_url.status != 200:  # URL-access check
            print("Can't load RSS feed.")
            raise Exception('RSS-reader failed. Status: {}.'.format(parsed_url.status))
        else:
            self.log('RSS parsed successfully')
            return parsed_url

    def information_about_site(self, parsed_url):
        """Function which make dictionary with data of website"""
        return {
            'Feed': parsed_url['feed']['title'],
            'Updated': parsed_url['updated'],
            'Version': parsed_url['version'],
        }

    def make_news_data(self, news):
        """
        Function which parsed HTML summary of news and make dictionary with all the necessary news data.
        :return dictionary
        """
        bs = BeautifulSoup(news['summary'], 'html.parser')
        img = bs.find_all('img')
        image_data = 'No image'
        if len(img) > 0:
            image_data = '{}\nSource of image: {}'.format(img[0]['alt'], img[0]['src'])
        news_summary = {
            'Title': news['title'],
            'Date': news['published'],
            'Summary': bs.get_text(),
            'Link': news['link'],
            'Image': image_data,
        }
        return news_summary

    def news_data_collection(self, parsed_url):
        """Function that collects data from all news by calling make_news_data.
        :return string of dictionaries
        """
        all_information_about_news = parsed_url['entries']
        # amount_of_news = len(parsed_url.entries)
        all_news = []
        self.log('News gathering')
        for news in all_information_about_news[:self.limit]:
            try:  # Exception when news is failed
                dictionary_of_news_data = self.make_news_data(news)
            except Exception as ex:
                self.log("Error processing news: {} {}".format(type(ex), ex))
                continue  # continues to process the following news
            else:
                all_news.append(dictionary_of_news_data)  # make list of dictionaries of news data for optional output
        return all_news

    def log(self, message):
        """Print time and log message if verbose is active."""
        if self.is_verbose:
            print(datetime.datetime.now(), message)

    def parse_to_json(self, dictionary):
        return json.dumps(dictionary, indent=4)

    def output(self, about_website, all_news):
        """Function which print information about site and a set of news."""
        print()
        for key, value in about_website.items():
            print(key, ': ', value)
            print()
        for number_of_news in all_news:
            print()
            for key, value in number_of_news.items():
                print(key, ': ', value)

    def output_json(self, about_website, all_news):
        print(self.parse_to_json([about_website] + all_news))

    def doing_everything_in_class(self):
        """Get news"""
        self.log('Start parsing')
        try:
            parsed_url = self.url_parsing()
            about_website = self.information_about_site(parsed_url)
        except Exception as ex:  # for any exception after website parsing
            self.log("Error reading site data: {}, {}".format(type(ex), ex))
            return
        string_of_news_dictionaries = self.news_data_collection(parsed_url)
        if self.is_json:
            self.log('Convert to JSON-format')
            self.output_json(about_website, string_of_news_dictionaries)
        else:
            self.log('Output news')
            self.output(about_website, string_of_news_dictionaries)


def arg_parse(args):
    """Function which parsed command-line arguments."""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument("source", type=str,
                        help="RSS URL")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT_COUNT,
                        help="Limit news topics if this parameter provided")
    parser.add_argument("--version", action="store_true",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    return parser.parse_args(args)


def main():
    args = arg_parse(sys.argv[1:])
    if args.version:
        print('RSS-reader version {}'.format(VERSION))  # program version call
        return
    reader = RSSReader(args.source)
    reader.limit = args.limit
    reader.is_verbose = args.verbose
    reader.is_json = args.json
    reader.doing_everything_in_class()


if __name__ == '__main__':
    main()
