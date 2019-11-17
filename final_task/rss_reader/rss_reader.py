#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log
import sqlite3
import rss_get_items
import arguments


def print_news(url: str, items):
    for item in items:
        print("Title: " + item['title'])
        print("Data: " + item['pubdate'])
        print("Link: " + item['link'])
        print("Description" + item['description'])
        print("URL" + item['url'])
        print('---')


def cacheNews(url):
    '''
    1. connect to database
    2. create table in database
    3. insert news into table
    '''


if __name__ == '__main__':
    received_args = args = arguments.command_line()
    link = received_args.URL
    limit = received_args.limit
    items = rss_get_items.get_items(link)

    if received_args.json:
        rss_get_items.get_json(items)

    if received_args.log_level:
        print(log.info)

    print_news(link, items)
