from collections import OrderedDict
from collections import defaultdict
import logging as log

import rss_get_items as filters


def split_string_by_lines(input_string: str, word_number: int) -> str:
    input_string = input_string.strip().split()
    result = ''
    for idx in range(len(input_string) // word_number + 1):
        start = idx * word_number
        end = (idx + 1) * word_number
        result += ' '.join(input_string[start: end]) + '\n'
    return result.strip()


def prepare_one_item(item_xml: defaultdict) -> OrderedDict:
    """" Take one rss item as dictionary and make ordered dict
    with title, date, description and media content"""
    title = item_xml['title']
    date = filters.pubdate(item_xml['pubDate'])
    date = data_split(date)
    news_link = item_xml['link']
    description = split_string_by_lines(
        filters.description(item_xml['description']),
        10
    )
    media_content = split_string_by_lines(
        ''.join(item_xml['content']),
        1
    )
    prepared_news = OrderedDict()

    prepared_news["Title:"] = title
    prepared_news["Date:"] = date
    prepared_news["Link: "] = news_link
    prepared_news["Description:\n"] = description
    prepared_news["Media content:\n"] = media_content
    return prepared_news


def print_one_item(news_item: OrderedDict) -> None:
    print("===Wow! News!===")
    for key, value in news_item.items():
        print(key, value)
    print("===End, news!===")


def print_news(items: list) -> None:
    """" Take list of rss items and print all this news"""
    log.info('Start print news')
    for item in items:
        item = prepare_one_item(item)
        print_one_item(item)
    log.info('End print news')


def make_json(items: list) -> dict:
    """convert article data in json format"""
    log.info('Start make json format')
    json = {}
    jsons = {}
    for idx, item in enumerate(items):
        for item in items:
            item = prepare_one_item(item)
            json = {
                'images': item['Media content:\n'],
                'link': item['Link: '],
                'description': item['Description:\n'],
                'date': item['Date:'],
                'title': item['Title:'],
         }
        jsons[idx] = json
    log.info('End make json format')
    return jsons


def print_json(items: list) -> None:
    json = make_json(items)
    log.info('Start print json')
    print("Json: {")
    for item, amount in json.items():
        print('"' + item + '":' + "{ " + amount + "}")
    log.info('End print json')


def data_split(date: str) -> str:
    month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    new_date = date
    new_date = (new_date.split(' ')[1:4])
    new_date[1] = month[new_date[1]]
    new_date = '/'.join(new_date)
    return new_date
