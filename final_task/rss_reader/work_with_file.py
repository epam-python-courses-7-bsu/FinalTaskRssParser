import datetime
import os
import json
import decorators


@decorators.functions_log
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


@decorators.functions_log
def read_feed_form_file(date_str: str):
    with open('cache.txt', 'r') as file:
        for line in file:
            if date_str in line:
                return json.loads(line[line.find(date_str) + len(date_str) + 1:].encode('UTF-8'))
        else:
            return 'Date ' + date_str + ' not found in cache.'
