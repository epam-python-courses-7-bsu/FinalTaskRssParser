"""Main module of the program"""

import RssReader.args_parser as args_parser
import RssReader.rss_parser as rss_parser
import RssReader.other as other
import RssReader.json_converter as json_converter
import RssReader.logs as logs
import sys


def main():
    """This is a main function"""
    print('============================== RSS Reader ==================================')
    logs.new_session()
    commands = args_parser.get_parse()

    while True:
        while True:

            """Print log journal"""
            if commands['verbose']:
                logs.log_print()
                logs.print_log()
                logs.end_session()
                sys.exit()

            """Check if URL looks like URL"""
            if args_parser.validate_url(commands['url']):
                logs.log_url(commands['url'])
            else:
                print('Invalid URL: check your URL.')
                print('(Example of valid URL: https://news.yahoo.com/rss/)')
                print('Enter valid URL (or enter "q" for quit, "-h" for help)')
                logs.log_wrong_url(commands['url'])

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Check if there is a server on other side"""
            if rss_parser.connect_rss(commands['url']):
                logs.log_connection(commands['url'])
            else:
                print('The server is not responding.')
                print('Enter new URL (or enter "q" for quit, "-h" for help)')
                logs.log_connection_failed(commands['url'])

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Check if URL is a RSS URL"""
            rss_news_raw = rss_parser.get_rss(commands['url'])
            if rss_news_raw:
                logs.log_rss(commands['url'])
            else:
                print('The RSS feed is not responding.')
                print('Check your URL (or enter "q" for quit, "-h" for help)')
                logs.log_wrong_rss(commands['url'])

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Check if all input arguments are valid"""
            if args_parser.validate_args(commands):
                pass
            else:
                print('Invalid input arguments.')
                print('Check your input parameters (or enter "q" for quit, "-h" for help)')

                choice = other.choice()
                commands = args_parser.get_parse(choice)
            break

        """Print the news and prepare data for further processing"""
        rss_news_clean = dict()
        for i in range(commands['limit']):
            if rss_parser.process_rss(rss_news_raw, i):
                rss_news_clean[i] = rss_parser.process_rss(rss_news_raw, i)
                if commands['json']:
                    json_converter.print_json((rss_news_clean[i]))
                else:
                    rss_parser.print_rss(rss_news_clean[i])
            else:
                print('Limit for news is reached.')
                break
            json_news = json_converter.convert_json(rss_news_clean)
        break

    logs.end_session()
    print('=====================End for news==============================')
