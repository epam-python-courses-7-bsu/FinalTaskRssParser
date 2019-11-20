#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rss_get_items
import arguments
import printers
import logging as log


def cacheNews(url):
    pass


if __name__ == '__main__':
    log.info('Start script')
    received_args = arguments.command_line()
    link = received_args.URL
    limit = received_args.limit
    items = rss_get_items.get_items(link)
    if limit is not None:
        log.info('User choose some limits')
        items = items[:limit]

    if received_args.json:
        log.info('User choose json format')
        printers.print_json(items)
    else:
        printers.print_news(items)

    #
    # if received_args.log_level:
    #     print(log.info)


