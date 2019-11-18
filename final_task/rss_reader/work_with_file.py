import datetime
import os
import json
import decorators
import RssReaderException


@decorators.functions_log
def add_feed_to_file(dict_data: dict):
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as read_file:
            dict_with_date = json.load(read_file)
    else:
        dict_with_date = {}
    for news_index, news_dict in enumerate(dict_data['items']):
        date = get_date(news_dict['published'])
        if date in dict_with_date.keys():
            links_on_news = []
            for dict_news in dict_with_date[date]['items']:
                links_on_news.append(dict_news['link'])
            if news_dict['link'] not in links_on_news:
                dict_with_date[date]['items'].append(news_dict)
        else:
            dict_with_date[date] = {
                                        'title': f"News by {news_dict['published'][:news_dict['published'].find(':') - 2]}",
                                        'items': [news_dict],
                                    }
    with open('cache.json', 'w') as file:
        json.dump(dict_with_date, file)


@decorators.functions_log
def read_feed_form_file(date_str: str):
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as read_file:
            dict_with_date = json.load(read_file)
        if date_str in dict_with_date.keys():
            return dict_with_date[date_str]
        else:
            raise RssReaderException.FileException('Date ' + date_str + ' not found in cache.')

    else:
        raise RssReaderException.FileException('Cache is empty. Please launch the app from the URL to the news site.\n'+\
                                               'EXAMPLE: rss-reader https://news.yahoo.com/rss')


def get_date(input_str: str) -> str:
    result = input_str[input_str.find(',') + 2: input_str.find(':') - 2].strip(' ')
    result = datetime.datetime.strptime(result, '%d %b %Y')
    return result.strftime('%Y%m%d')
