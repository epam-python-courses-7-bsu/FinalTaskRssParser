import argparse
import feedparser
import logging
import json
import html
import sys
import datetime

__version__ = '3.5'
args = None
limit = 3
links = []
print_setting = {
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


def get_object_feed(url: str):
    try:
        data = feedparser.parse(url)
        # if data.status == 200:
        if data.bozo:
            return f'There is no rss feed at this url: {url}'
        else:
            return data
        # else:
        #     return f'HTTP Status Code {data.status}'
    except Exception as exc:
        return f'ERROR: {exc}'


def to_json(data, **kwargs):
    # convert data to JSON format
    result = {}
    if 'feed' in kwargs.keys():
        for i in kwargs['feed']:
            result[i] = data['feed'][i]
    if 'entries' in kwargs.keys():
        result['items'] = []
        for i in range(int(limit)):
            temp = {}
            for j in kwargs['entries']:
                temp[j] = data['entries'][i][j]
            result['items'].append(temp)
    result = json.dumps(result)
    return html.unescape(result)


def get_img(input_string):
    # from string type '<img src="link" alt="something">text' returns ('link', 'something')
    input_string = input_string[input_string.find('<img'):]
    link = input_string[input_string.find('src="') + 5:]
    str_img = input_string[input_string.find('alt="') + 5:]
    return link[:link.find('"')], str_img[:str_img.find('"')]


def text_for_print(key, string):
    # processes a string for output
    global links
    if '<' not in string:
        return key[0].upper() + key[1:] + ': ' + html.unescape(string)
    if 'img' in string:
        image_link_and_alt_text = get_img(string)
        links.append(image_link_and_alt_text[0])
        image = '[image ' + str(len(links)) + ': ' + image_link_and_alt_text[1] + '][' + str(len(links)) + '] '
    string = string[string.find('<') + 1:]
    while string.find('<') - string.find('>') < 2:
        string = string[string.find('>') + 2:]
    string = string[string.find('>') + 1:string.find('<')]
    return key[0].upper() + key[1:] + ':' + image + html.unescape(string)


def set_start_setting():
    # setup start settings
    global args, limit
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided")
    parser.add_argument("--date", help="Obtaining the cached news without the Internet")
    args = parser.parse_args()
    if args.limit:
        limit = args.limit
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    else:
        logging.basicConfig(filename="sample.log", level=logging.INFO)


def beautiful_print_data(data, **kwargs):
    logging.info(type(data))
    if type(data) == feedparser.FeedParserDict:
        if args.json:
            data = to_json(data, **kwargs)
            print(data)
        else:
            print()
            for i in kwargs['feed']:
                print(data['feed'][i])
            print()
            k = 1
            for i in range(int(limit)):
                for j in kwargs['entries']:
                    print(text_for_print(j, data['entries'][i][j]))
                print()
            print()
            print('Links:')
            for i, v in enumerate(links):
                print(f'[{i + 1}]{v}')
            print()
    elif type(data) == dict:
        print()
        for i in kwargs['feed']:
            print(data[i])
        print()
        k = 1
        for i in range(int(limit)):
            for j in kwargs['entries']:
                print(text_for_print(j, data['items'][i][j]))
            print()
        print()
        print('Links:')
        for i, v in enumerate(links):
            print(f'[{i + 1}]{v}')
        print()
    elif type(data) == str:
        print(data)


def add_feed_to_file(json_data):
    date_str = datetime.datetime.now().date().strftime('%Y%m%d')
    try:
        with open('cache.txt', 'r') as fin:
            lines = fin.readlines()
    except FileNotFoundError:
        lines = []
    with open('cache.txt', 'w') as file:
        if not lines:
            file.write(datetime.datetime.now().date().strftime('%Y%m%d') + ' ' + str(json_data) + '\n')
        for line in lines:
            if date_str in line:
                file.write(datetime.datetime.now().date().strftime('%Y%m%d') + ' ' + str(json_data) + '\n')
            else:
                file.write(line)


def read_feed_form_file(date_str):
    with open('cache.txt', 'r') as file:
        for i in file:
            if date_str in i:
                return json.loads(i[i.find(date_str) + len(date_str) + 1:].encode('UTF-8'))
        else:
            return 'Date ' + date_str + ' not found in cache.'
    return None


def run():
    set_start_setting()
    if args.version:
        print(f'RSS reader version {__version__}')
    elif args.date:
        beautiful_print_data(read_feed_form_file(args.date), **print_setting)
    else:
        data = get_object_feed(args.source)
        if type(data) == feedparser.FeedParserDict:
            add_feed_to_file(to_json(data, **print_setting))
        beautiful_print_data(data, **print_setting)


if __name__ == '__main__':
    run()
