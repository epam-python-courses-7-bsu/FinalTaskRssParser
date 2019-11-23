#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log
import sys
import datetime
import arguments
import printers
import rss_get_items
import converting


now = datetime.datetime.now()

""" Set basic configs for logging """
stdoutHandler = log.StreamHandler(sys.stdout)
fileHandler = log.FileHandler("logging.log", "a", encoding="utf-8")
log.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s',
                level=log.DEBUG,
                handlers=[fileHandler])


def print_verbose() -> None:
    log.info('try to read log file')
    with open('logging.log', 'r', encoding="utf-8") as f:
        print(f.read())


def get_txt_date(data) -> None:
    date_id = {}
    with open('dates.txt', 'r', encoding="utf-8") as f:
        for line in f:
            key, *value = line.split()
            date_id[key] = value
    # len_txt_date = len(date_id)
    if data == date_id[key]:
        date_id[key] = value
        with open('{}.txt'.format(value), 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("There isn't any news from this day")


def cash_news() -> None:
    log.info('Try to cash news from stdout')
    data_id = {}
    data = now.strftime("%d/%m/%Y")
    with open('dates.txt', 'r', encoding="utf-8") as f:
        for line in f:
            key, *value = line.split()
            data_id[key] = value
    len_txt_date = len(data_id) + 1
    remembered_data = {}
    with open('dates.txt', 'w', encoding='utf-8') as f:
        remembered_data[data] = len_txt_date
        f.write(str(remembered_data))
    # with open('{}.txt'.format(remembered_data[data]),
    # 'w', encoding='utf-8') as f:


if __name__ == '__main__':
    log.info('Start script')
    received_args = arguments.command_line()
    link = received_args.URL
    limit = received_args.limit
    date = received_args.date
    items = rss_get_items.get_items(link)

    if limit is not None:
        log.info('User choose some limits')
        items = items[:limit]

    if received_args.json:
        log.info('User choose json format')
        printers.print_json(items)
    else:
        printers.print_news(items)
        #cash_news()

    if received_args.verbose:
        log.info('User choose verbose')
        print_verbose()

    if received_args.html:
        log.info('User choose html')
        converting.write_to_file(items)

    if received_args.pdf:
        log.info('User choose pdf')
        converting.create_pdf(items)

    if date is not None:
        get_txt_date(date)
