"""
This module process the news cashing and storing
"""

import os

this_directory = os.path.abspath(os.path.dirname(__file__))
newsLog = 'news.log'
directory = os.path.join(this_directory, newsLog)

def news_check(rss_news: dict) -> bool:
    """This function checks, if the news is inside the local storage"""
    try:
        with open(directory, encoding='utf-8') as file:
            for line in file:
                if rss_news['link'] in line:
                    return False
        return True
    except FileNotFoundError:
        return True

def news_store(rss_news: dict):
    """This function stores the news to the dictionary"""
    with open(directory, 'a+', encoding='utf-8') as file:
        file.write('!!!#####STARTOFNEWS#####!!!' + rss_news['news_date'] + '\n')
        file.write('Feed: ' + rss_news['feed'] + '\n')
        file.write('Title: ' + rss_news['title'] + '\n')
        file.write('Date: ' + rss_news['date'] + '\n')
        file.write('Link: ' + rss_news['link'] + '\n')
        file.write('Image: ' + rss_news['image'] + '\n')
        file.write(' ' + '\n')
        file.write(rss_news['description'])
        file.write('. . . . . . . . . . . . . . . . . . .' + '\n')
        file.write('!!!#####ENDOFNEWS#####!!!' + rss_news['news_date'] + '\n')


def news_print(date: str, limit: int) -> int:
    """This function prints the news from local storage with specified [date]"""
    flag = False
    empty = True
    counter = 0
    try:
        with open(directory, 'r', encoding='utf-8') as file:
            for line in file:
                if '!!!#####ENDOFNEWS#####!!!'+date in line:
                    flag = False

                if flag:
                    print(line, end='')
                    empty = False

                if '!!!#####STARTOFNEWS#####!!!'+date in line:
                    flag = True

                    if counter == limit:
                        return 3

                    if limit != -1:
                        counter += 1
    except FileNotFoundError:
        print('Error: File not found. (Maybe this is a first time you are running a program)')
        return 1

    if empty:
        print('Error: news with ' + date + ' not found.')
        return 2

    return 0


def news_decompose(date: str, limit: int):
    """This function takes the news from local storage"""
    flag = False
    empty = True
    counter_news = 0
    counter_lines = 0
    counter = 0
    news = dict()
    dict_buffer = dict()
    news_buffer = list()
    string_buffer = ''

    try:
        with open(directory, 'r', encoding='utf-8') as file:
            for line in file:
                if '!!!#####ENDOFNEWS#####!!!' + date in line:
                    flag = False

                    if string_buffer:
                        dict_buffer['description'] = string_buffer
                        news[counter_news] = dict_buffer
                        counter_news += 1

                    counter_lines = 0
                    news_buffer = list()
                    dict_buffer = dict()
                    string_buffer = ''

                if flag:
                    empty = False
                    if counter_lines < 5:
                        news_buffer.append(line)
                        counter_lines += 1
                    elif counter_lines == 5:
                        dict_buffer['feed'] = news_buffer[0].replace('Feed: ', '').replace('\n', '')
                        dict_buffer['title'] = news_buffer[1].replace('Title: ', '').replace('\n', '')
                        dict_buffer['date'] = news_buffer[2].replace('Date: ', '').replace('\n', '')
                        dict_buffer['link'] = news_buffer[3].replace('Link: ', '').replace('\n', '')
                        dict_buffer['image'] = news_buffer[4].replace('Image: ', '').replace('\n', '')
                        counter_lines += 1
                    else:
                        string_buffer += line

                if '!!!#####STARTOFNEWS#####!!!' + date in line:
                    flag = True

                    if counter == limit:
                        return news

                    if limit != -1:
                        counter += 1

        if empty:
            print('Error: news with ' + date + ' not found.')
            news[0] = 2
            return news

        return news

    except FileNotFoundError:
        print('Error: File not found. (Maybe this is a first time you are running a program)')
        news[0] = 1
        return news








