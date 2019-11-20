import logging
import json


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


def print_news_JSON(news_list):
    """
        :param news_list: The list of news
        Prints news in readable JSON format
        """
    logging.info('Printing news as JSON')
    print(json.dumps(news_list, ensure_ascii=False, indent=4))
