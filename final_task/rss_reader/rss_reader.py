import argparse
from typing import Union

import feedparser
import logging
import json
import html
import sys
import datetime
import os

__VERSION__ = '3.5'
ARGS = None
LIMIT = 3
LINKS = []
PRINT_SETTING = {
    'feed': [
        'title'
    ],
    'entries': [
        'title',
        'published',
        'link',
        'summary'
    ]
}


def get_object_feed(url: str) -> Union[str, feedparser.FeedParserDict]:
    try:
        data = feedparser.parse(url)
        if data.status == 200:
            if data.bozo:
                return f'ERROR: There is no rss feed at this url: {url}'
            else:
                return data
        else:
            return f'HTTP Status Code {data.status}'
    except Exception as exc:
        return f'ERROR: {exc}'


def to_json(data) -> json:
    """convert data to JSON format"""
    result = {}
    if isinstance(data, feedparser.FeedParserDict):
        if 'feed' in PRINT_SETTING.keys():
            for feed_element in PRINT_SETTING['feed']:
                result[feed_element] = text_processing(data['feed'][feed_element])
        if 'entries' in PRINT_SETTING.keys():
            result['items'] = []
            for index_news in range(LIMIT):
                temp = {}
                for items_element in PRINT_SETTING['entries']:
                    temp[items_element] = text_processing(data['entries'][index_news][items_element])
                result['items'].append(temp)
        result['links'] = LINKS
    result = json.dumps(result)
    return result


def get_img(input_string: str) -> [str, str]:
    """from string type '<img src="link" alt="something">text' returns ['link', 'something']"""
    input_string = input_string[input_string.find('<img'):]
    link = input_string[input_string.find('src="') + 5:]
    str_img = input_string[input_string.find('alt="') + 5:]
    return [link[:link.find('"')], str_img[:str_img.find('"')]]


def text_processing(string):
    """processes a string for output"""
    global LINKS
    image = ''
    if '<' not in string:
        return html.unescape(string)
    if 'img' in string:
        image_link_and_alt_text = get_img(string)
        LINKS.append(image_link_and_alt_text[0])
        image = '[image ' + str(len(LINKS)) + ': ' + image_link_and_alt_text[1] + '][' + str(len(LINKS)) + '] '
    string = string[string.find('<') + 1:]
    while string.find('<') - string.find('>') < 2:
        string = string[string.find('>') + 2:]
    string = string[string.find('>') + 1:string.find('<')]
    return image + html.unescape(string)


def set_start_setting():
    """setup start settings"""
    global ARGS, LIMIT
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("--date", help="Obtaining the cached news without the Internet")
    ARGS = parser.parse_args()
    if ARGS.limit:
        LIMIT = ARGS.limit
    if ARGS.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    else:
        logging.basicConfig(filename="sample.log", level=logging.INFO)


def add_feed_to_file(json_data: json):
    date_str = datetime.datetime.now().date().strftime('%Y%m%d')
    lines = []
    if os.path.exists('./cache.txt'):
        with open('cache.txt', 'r') as fin:
            lines = fin.readlines()
    flag = True
    with open('cache.txt', 'w') as file:
        if not lines:
            file.write(date_str + ' ' + str(json_data) + '\n')
            flag = False
        for line in lines:
            if date_str in line:
                file.write(date_str + ' ' + str(json_data) + '\n')
                flag = False
            else:
                file.write(line)
    if flag:
        file.write(date_str + ' ' + str(json_data) + '\n')

def read_feed_form_file(date_str: str):
    with open('cache.txt', 'r') as file:
        for line in file:
            if date_str in line:
                return json.loads(line[line.find(date_str) + len(date_str) + 1:].encode('UTF-8'))
        else:
            return 'Date ' + date_str + ' not found in cache.'


def get_string_with_result(data: json) -> str:
    """Converts json to string for print"""
    result = ''
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                result += '\n' + value + '\n\n'
                continue
            if isinstance(value, list) and key != 'items':
                result += '\n' + edit_key(key) + '\n'
            for item in value:
                if isinstance(item, dict):
                    for key_l, value_l in item.items():
                        result += edit_key(key_l) + value_l
                        result += '\n'
                else:
                    result += item
                result += '\n'
    else:
        result = data
    return result


def edit_key(input_key: str) -> str:
    if input_key == 'published':
        input_key = 'Date'
    elif input_key == 'summary':
        input_key = 'Description'
    return input_key[0].upper() + input_key[1:] + ': '


def run():
    set_start_setting()
    if ARGS.version:
        print(f'RSS reader version {__VERSION__}')
    elif ARGS.date:
        print(get_string_with_result(read_feed_form_file(ARGS.date)))
    else:
        data = get_object_feed(ARGS.source)
        data = to_json(data)
        add_feed_to_file(data)
        if ARGS.json:
            print(json.loads(data))
        else:
            print(get_string_with_result(json.loads(data)))


if __name__ == '__main__':
    run()