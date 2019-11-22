import logging
import json
from colorama import Fore, Back, Style


def print_news(news_list):
    """
    :param news_list: The list of news
    Prints news in readable format
    """
    logging.info('Printing news')
    for index, new in enumerate(news_list):
        print(f'New {index + 1}\n')
        print(f'Feed:\n\t{new["Feed"]}')
        print('Title:')
        print(f'\t{new["Title"]}')
        print(f'Date:\n\t{new["Date"]}')
        print(f'Link:\n\t{new["Link"]}')
        print(f'Image description:\n\t{new["Image description"]}')
        print(f'New description:\n\t{new["New description"]}')
        print('Image links:')
        for image_link in new['Image links']:
            print(f'\t{image_link}')
        print('\n')


def print_news_colorize(news_list):
    """
    :param news_list: The list of news
    Prints news in readable colorize format
    """
    logging.info('Printing news colorize')
    for index, new in enumerate(news_list):
        print(Style.RESET_ALL + Fore.WHITE + Back.MAGENTA + f'New {index + 1}\n')
        print(Style.RESET_ALL + Fore.WHITE + Back.BLUE + 'Feed:\n' + Style.RESET_ALL + Fore.BLUE + f'\t{new["Feed"]}')
        print(
            Style.RESET_ALL + Fore.WHITE + Back.GREEN + 'Title:\n' + Style.RESET_ALL + Fore.GREEN + f'\t{new["Title"]}')
        print(Style.RESET_ALL + Fore.WHITE + Back.CYAN + 'Date:\n' + Style.RESET_ALL + Fore.CYAN + f'\t{new["Date"]}')
        print(Style.RESET_ALL + Fore.WHITE + Back.RED + 'Link:\n' + Style.RESET_ALL + Fore.RED + f'\t{new["Link"]}')
        print(
            Style.RESET_ALL + Fore.WHITE + Back.YELLOW + 'Image description:\n' + Style.RESET_ALL + \
            Fore.YELLOW + f'\t{new["Image description"]}')
        print(
            Style.RESET_ALL + Fore.WHITE + Back.LIGHTBLUE_EX + 'New description:\n' + Style.RESET_ALL + \
            Fore.LIGHTBLUE_EX + f'\t{new["New description"]}')
        print(Style.RESET_ALL + Fore.BLACK + Back.LIGHTGREEN_EX + 'Image links:')
        for image_link in new['Image links']:
            print(Style.RESET_ALL + Fore.LIGHTGREEN_EX + f'\t{image_link}')
        print('\n')


def print_news_JSON(news_list):
    """
        :param news_list: The list of news
        Prints news in readable JSON format
        """
    logging.info('Printing news as JSON')
    print(json.dumps(news_list, ensure_ascii=False, indent=4))


def print_news_JSON_colorize(news_list):
    """
        :param news_list: The list of news
        Prints news in readable colorize JSON format
        """
    logging.info('Printing news as JSON')
    result_str = "["
    for new_index, new in enumerate(news_list):
        result_str += f"\n\t\n\t\t\"\033[41mFeed\033[0m\": \"\033[31m{new['Feed']}\033[0m\"," \
                      f"\n\t\t\"\033[42mTitle\033[0m\": \"\033[32m{new['Title']}\033[0m\"," \
                      f"\n\t\t\"\033[43mDate\033[0m\": \"\033[33m{new['Date']}\033[0m\"," \
                      f"\n\t\t\"\033[44mLink\033[0m\": \"\033[34m{new['Link']}\033[0m\"," \
                      f"\n\t\t\"\033[45mImage description\033[0m\": \"\033[35m{new['Image description']}\033[0m\"," \
                      f"\n\t\t\"\033[46mNew description\033[0m\": \"\033[36m{new['New description']}\033[0m\"," \
                      f"\n\t\t\"\033[44mImage links\033[0m\": ["
        for link_index, link in enumerate(new['Image links']):
            result_str += f"\n\t\t\t\"\033[34m{link}\033[0m\""
            if link_index + 1 != len(new['Image links']):
                result_str += ','
        result_str += "\n\t\t]\n\t}"
        if new_index + 1 != len(news_list):
            result_str += ','
    result_str += '\n]'
    print(result_str)
