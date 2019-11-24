import json
import logging
from urllib.error import URLError
import parser_rss
from pars_args import get_args
import colorama
from colorama import Fore, Back, Style


def print_news_in_json(list_of_news: list):
    """
    This function print news in the console in json format
    :param list_of_news:
    :return:
    """
    logger = logging.getLogger("rss_reader.parser_rss.print_news_in_json")
    logger.info("print news in the console in json format")
    list_of_news_in_json = []
    for news in list_of_news:
        list_of_news_in_json.append(news.get_json())
    print(json.dumps(list_of_news_in_json, indent=4, ensure_ascii=False))


def print_news_without_cashing():
    try:
        args = get_args()
        list_of_news = []
        news_feed = parser_rss.get_news_feed(args.source)
        parser_rss.init_list_of_news(list_of_news, news_feed, args.limit)
        if args.json:
            print_news_in_json(list_of_news)
        else:
            print_news(list_of_news)
    except URLError as er:
        print(er)
    except Exception as e:
        print(e)


def print_news(list_of_news: list):
    """
    This function print news in the console
    :param feed_title:
    :param list_of_news:
    :return:
    """
    logger = logging.getLogger("rss_reader.parser_rss.print_news")
    logger.info("print news in the console")
    for number, news in enumerate(list_of_news):
        print(number + 1)  # because number starts at 0
        print(news)
        print('-' * 100)


def print_news_in_multi_colored_format(list_of_news: list):
    colorama.init()
    for number, news in enumerate(list_of_news):
        links = ""
        for index, link in enumerate(news.links_from_news or []):
            links += "[" + str(index) + "] " + link + "\n"
        print('\033[1m\033[32m\033[4m' + str(number + 1) + ":")
        print(Style.RESET_ALL + Fore.BLUE + f'Feed: {news.feed}')
        print(Style.RESET_ALL + Fore.GREEN + f'Title: {news.title}')
        print(Style.RESET_ALL + Fore.YELLOW + f'Date: {news.date}')
        print(Style.RESET_ALL + Fore.CYAN + f'Link: {news.link}')
        print(Style.RESET_ALL + Fore.YELLOW + f'Info about image: {news.info_about_image}')
        print(Style.RESET_ALL + Fore.GREEN + f'Briefly about news: {news.briefly_about_news}')
        print(Style.RESET_ALL + Fore.CYAN + f'Links: \n{links}')


def print_news_in_json_in_multi_colored_format(list_of_news: list):
    result = "\033[1m\033[35m[\033[0m\n"
    for number, news in enumerate(list_of_news):

        result += "    \033[1m\033[31m{\033[0m\n"
        result += f'''        \033[1m\033[34m"Feed": "{news.feed}",\033[0m\n'''
        result += f'''        \033[32m"Title": "{news.title}",\033[0m\n'''
        result += f'''        \033[33m"Date": "{news.date}",\033[0m\n'''
        result += f'''        \033[36m"Link": "{news.link}",\033[0m\n'''
        result += f'''        \033[33m"Info about image": "{news.info_about_image}",\033[0m\n'''
        result += f'''        \033[32m"Briefly about news": "{news.briefly_about_news}",\033[0m\n'''
        result += f'''        \033[36m"Links": [\n'''
        for index_link, link in enumerate(news.links_from_news):
            result += f'''            "{link}"'''
            if index_link != len(news.links_from_news) - 1:
                result += ',\n'
        result += '\n'
        result += "        ]\033[0m\n"
        result += "    \033[1m\033[31m}\033[0m"
        if len(list_of_news) - 1 != number:
            result += ','
        result += '\n'

    result += "\033[1m\033[35m]\033[0m"
    print(result)
