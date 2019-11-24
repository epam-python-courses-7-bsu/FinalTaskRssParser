"""Main module of the program"""

import sys
import os

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(THIS_DIRECTORY)


import args_parser
import rss_parser
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

    """Check if all input arguments are valid"""
    if args_parser.validate_args(commands):
        pass
    else:
        print('Invalid input arguments.')
        print('Check your input parameters')
        logs.log_invalid_arguments(str(commands))

        return 1

    """Print log journal"""
    if commands['verbose'] and (not commands['pdf']) and (not commands['html']):
        logs.log_print()
        logs.print_log()

        return 0

    """Convert log to pdf"""
    if commands['verbose'] and commands['pdf']:
        logs.print_log_verbose_pdf()
        log_journal = logs.log_prepare()
        converter.convert_log_pdf(log_journal, commands['pdf'])
        logs.log_log_pdf()
        print('Log journal was converted to pdf')

        return 0

    """Convert log to html"""
    if commands['verbose'] and commands['html']:
        logs.print_log_verbose_html()
        log_journal = logs.log_prepare()
        converter.convert_log_html(log_journal, commands['html'])
        logs.log_log_html()
        print('Log journal was converted to html')

        return 0

    """Print news log from history"""
    if commands['date'] and (commands['pdf'] is None) and (commands['html'] is None) and (commands['json'] is None):
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

        return 0

    """Print news from history in json format"""
    if commands['date'] and (commands['json']) and (commands['pdf'] is None) and (commands['html'] is None):
        if commands['limit']:
            news_tryout = news.news_decompose(str(commands['date']), commands['limit'])
        else:
            news_tryout = news.news_decompose(str(commands['date']), -1)

        json_converter.print_json(news_tryout)

        return 0

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

        return 0

    """Convert news from history to html"""
    if commands['date'] and commands['html']:
        if commands['limit']:
            decompose_tryout = news.news_decompose(str(commands['date']), commands['limit'])
        else:
            decompose_tryout = news.news_decompose(str(commands['date']), -1)

        if decompose_tryout[0] == 1:
            logs.log_news_filenotfound()
        elif decompose_tryout[0] == 2:
            logs.log_news_print_err()
        else:
            converter.convert_html(decompose_tryout, commands['html'])

        logs.log_news_local_storage_html()
        print('News from local storage were converted to html.')

        return 0

    """Check if URL looks like URL"""
    if args_parser.validate_url(commands['url']):
        logs.log_url(commands['url'])
    else:
        print('Invalid URL: check your URL.')
        print('(Example of valid URL: https://news.yahoo.com/rss/)')
        print('Enter valid URL')
        logs.log_wrong_url(commands['url'])

        return 1

    """Check if there is a server on other side"""
    if rss_parser.connect_rss(commands['url']):
        logs.log_connection(commands['url'])
    else:
        print('Enter new URL')
        logs.log_connection_failed(commands['url'])

        return 1

    """Check if URL is a RSS URL"""
    rss_news_raw = rss_parser.get_rss(commands['url'])
    if rss_news_raw:
        logs.log_rss(commands['url'])
        news_limit = len(rss_news_raw.entries)
    else:
        print('The RSS feed is not responding.')
        print('Check your URL')
        logs.log_wrong_rss(commands['url'])

        return 1

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
            elif not commands['pdf'] and not commands['html']:
                rss_parser.print_rss(rss_news_clean[i])
        else:
            print('Limit for news is reached.')

    """Write the news to file"""
    for value in rss_news_clean.values():
        if news.news_check(value):
            news.news_store(value)
            logs.log_news_store(value['link'])
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

    """Create html file"""
    if commands['html'] and rss_news_clean:
        converter.convert_html(rss_news_clean, commands['html'])
        logs.log_news_html()
        print("News were converted to html")

    logs.end_session()
    print('============================= End for news =================================')


if __name__ == '__main__':
    main()
