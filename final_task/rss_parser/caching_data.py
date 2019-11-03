import json
import datetime


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
