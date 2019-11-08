"""
This module process the news cashing and storing
"""

import os

this_directory = os.path.abspath(os.path.dirname(__file__))
newsLog = 'news.log'
directory = os.path.join(this_directory, newsLog)


def news_store(rss_news: dict):
    """This function stores the news to the dictionary"""
    with open(directory, 'a+') as file:
        for value in rss_news.values():
            file.write('!!!#####STARTOFNEWS#####!!!' + value['news_date'] + '\n')
            file.write('Feed: ' + value['feed'] + '\n')
            file.write('Title: ' + value['title'] + '\n')
            file.write('Date: ' + value['date'] + '\n')
            file.write('Link: ' + value['link'] + '\n')
            file.write(' ' + '\n')
            file.write(value['description'])
            file.write('. . . . . . . . . . . . . . . . . . .' + '\n')
            file.write('!!!#####ENDOFNEWS#####!!!' + value['news_date'] + '\n')
        file.close()


def news_print(date: str) -> int:
    """This function prints the news from local storage with specified [date]"""
    flag = False
    empty = True
    try:
        with open(directory, 'r') as file:
            for line in file:
                if '!!!#####ENDOFNEWS#####!!!'+date in line:
                    flag = False

                if flag:
                    print(line, end='')
                    empty = False

                if '!!!#####STARTOFNEWS#####!!!'+date in line:
                    flag = True
    except FileNotFoundError:
        print('Error: File not found. (Maybe this is a first time you are running a program)')
        return 1

    if empty:
        print('Error: news with ' + date + ' not found.')
        return 2

    return 0






