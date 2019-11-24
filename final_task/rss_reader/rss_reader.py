#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log
import sys
import datetime
import arguments
import printers
import rss_get_items
import converting
import DatabaseEmulation
from copy import deepcopy

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


if __name__ == '__main__':

    log.info("Start script")

    database = DatabaseEmulation.DatabaseEmulation(
        '_database/dates.txt', '_database/data'
    )

    received_args = arguments.command_line()
    link = received_args.URL
    limit = received_args.limit
    date = received_args.date

    all_items = None

    if date is not None:
        if database.check_date(date):
            idx = database.get_id(date)
            all_items = database.get_items(idx)
        else:
            print("Nothing by this date")
            sys.exit()
    else:
        all_items = rss_get_items.get_items(link)

    items = deepcopy(all_items)

    if limit is not None:
        log.info("User choose some limits")
        items = all_items[:limit]

    if received_args.json:
        log.info("User choose json format")
        printers.print_json(items)
    else:
        printers.print_news(items)
        database.write_items(all_items)

    if received_args.verbose:
        log.info("User choose verbose")
        print_verbose()

    if received_args.html:
        log.info("User choose html")
        converting.write_to_file(items)

    if received_args.pdf:
        log.info("User choose pdf")
        converting.create_pdf(items)
