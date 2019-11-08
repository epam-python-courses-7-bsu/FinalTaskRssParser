"""Main module of the program"""

import sys
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_directory)


import logs
import args_parser
import rss_parser
import other
import json_converter
import news


def main():

    """This is a main function"""
    print('============================== RSS Reader ==================================')
    logs.new_session()
    commands = args_parser.get_parse()

    while True:
        while True:

            """Check if all input arguments are valid"""
            if args_parser.validate_args(commands):
                pass
            else:
                print('Invalid input arguments.')
                print('Check your input parameters (or enter "q" for quit, "-h" for help)')
                logs.log_invalid_arguments(str(commands))

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Print log journal"""
            if commands['verbose']:
                logs.log_print()
                logs.print_log()
                logs.end_session()
                sys.exit()

            """Print news log from history"""
            if commands['date']:
                print_tryout = news.news_print(str(commands['date']))
                if print_tryout == 0:
                    logs.log_news_print()
                elif print_tryout == 1:
                    logs.log_news_filenotfound()
                elif print_tryout == 2:
                    logs.log_news_print_err()
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

            break

        """Print the news and prepare data for further processing
           "i" is a running index. 
        """
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

        """Write the news to file"""
        news.news_store(rss_news_clean)
        logs.log_news_store()
        break

    logs.end_session()
    print('=====================End for news==============================')


if __name__ == '__main__':
    main()




