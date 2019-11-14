"""Main module of the program"""

import sys
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_directory)


import args_parser
import rss_parser
import other
import json_converter
import converter
import logs
import news
import ast


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
            if commands['verbose'] and (not commands['pdf']):
                logs.log_print()
                logs.print_log()
                print('Would you like to continue? (enter the url or enter "q" for quit, "-h" for help)')

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Convert log to pdf"""
            if commands['verbose'] and commands['pdf']:
                log_journal = logs.log_prepare()
                converter.convert_log_pdf(log_journal, commands['pdf'])
                print('Log journal was converted to pdf')
                print('Would you like to continue? (enter the url or enter "q" for quit, "-h" for help)')

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Print news log from history"""
            if commands['date'] and (commands['pdf'] is None):
                if commands['limit']:
                    print_tryout = news.news_print(str(commands['date']), commands['limit'])
                else:
                    print_tryout = news.news_print(str(commands['date']), -1)

                if print_tryout == 0:
                    logs.log_news_print()
                elif print_tryout == 1:
                    logs.log_news_filenotfound()
                elif print_tryout == 2:
                    logs.log_news_print_err()
                elif print_tryout == 3:
                    logs.log_news_limit(commands['limit'])
                print('Would you like to continue? (enter the url or enter "q" for quit, "-h" for help)')

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

            """Convert news from history to pdf"""
            if commands['date'] and commands['pdf']:
                if commands['limit']:
                    decompose_tryout = news.news_decompose(str(commands['date']), commands['limit'])
                else:
                    decompose_tryout = news.news_decompose(str(commands['date']), -1)

                if decompose_tryout[0] == 1:
                    logs.log_news_filenotfound()
                elif decompose_tryout[0] == 2:
                    logs.log_news_print_err()
                else:
                    converter.convert_pdf(decompose_tryout, commands['pdf'])

                logs.log_news_local_storage_pdf()
                print('News from local storage were converted to pdf.')
                print('Would you like to continue? (enter the url or enter "q" for quit, "-h" for help)')

                choice = other.choice()
                commands = args_parser.get_parse(choice)
                continue

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
                news_limit = len(rss_news_raw.entries)
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

        """Check if we out of range in news limit, if yes we print all news, if no, we print 'limit' news"""
        if commands['limit'] and (commands['limit'] <= news_limit):
            limit = commands['limit']
        else:
            limit = news_limit

        for i in range(limit):
            if rss_parser.process_rss(rss_news_raw, i):
                rss_news_clean[i] = rss_parser.process_rss(rss_news_raw, i)
                if commands['json'] and (not commands['pdf']):
                    json_converter.print_json((rss_news_clean[i]))
                elif not commands['pdf']:
                    rss_parser.print_rss(rss_news_clean[i])
            else:
                print('Limit for news is reached.')
                break

        """Write the news to file"""
        for value in rss_news_clean.values():
            if news.news_check(value):
                news.news_store(value)
                logs.log_news_store()
            else:
                logs.log_news_copycat(value['link'])

        """Create pdf file"""
        if commands['pdf'] and rss_news_clean and (not commands['json']):
            converter.convert_pdf(rss_news_clean, commands['pdf'])
            logs.log_news_pdf()
            print("News were converted to pdf")

        if commands['pdf'] and commands['json']:
            json_news = ast.literal_eval(json_converter.convert_json(rss_news_clean))
            converter.convert_pdf(json_news, commands['pdf'])
            logs.log_news_pdf()
            print("News were converted to pdf")

        break

    logs.end_session()
    print('=====================End for news==============================')


if __name__ == '__main__':
    main()