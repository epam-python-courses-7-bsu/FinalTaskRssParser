from tools import merge_lists
from exceptions import StorageNotFoundError, NewsNotFoundError
from datetime import datetime
from items import ItemGroup
import pickle
import logging


def save_news(news_source, items_group, file_name):
    """ Save news in storage

    Existing news will not be repeated.

    :param news_source: url of RSS
    :type news_source: str

    :type items_group: 'items.ItemGroup'

    :param file_name: storage file
    :type file_name: str
    """
    logging.info('Reading news from file named ' + file_name)
    try:
        with open(file_name, 'rb') as f:
            news = dict(pickle.load(f))
    except FileNotFoundError:
        news = dict()

    logging.info('Adding current news to news from file.')
    if news_source in news.keys():
        unique_news = merge_lists(news[news_source].items, items_group.items)
        news[news_source].items = unique_news
    else:
        news[news_source] = items_group

    logging.info('Writing news in file named ' + file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(news, f)


def get_news_by_date(date, file_name, source=None, limit=None):
    """ Retrieve and return news by date from storage

    If source is specified return news from this source.
    If limit is specified return limited count of news.

    :param date: date of news publishing
    :type date: 'datetime.datetime'

    :param file_name: storage file
    :type file_name: str

    :param source: url of RSS
    :type source: str

    :param limit: limited count of returned news
    :type limit: int

    :rtype: list of 'items.ItemGroup'
    """
    logging.info('Reading news from file named ' + file_name)
    try:
        with open(file_name, 'rb') as f:
            news = dict(pickle.load(f))
    except FileNotFoundError:
        raise StorageNotFoundError(file_name)

    logging.debug('source = ' + (source or 'None'))
    logging.debug('limit = ' + (str(limit) or 'None'))
    logging.info('Retrieving news by date ' + str(date))

    list_of_news = list()
    if source and source in news.keys():
        item_group_by_date = retrieve_news_by_date(date, news[source], limit)

        if item_group_by_date.items:
            list_of_news.append(ItemGroup(feed=item_group_by_date.feed, items=item_group_by_date.items))

    elif not source:
        list_of_news = retrieve_news_by_date_from_list(date, news.values(), limit)
    else:
        raise NewsNotFoundError(date, file_name, source)

    if not list_of_news:
        raise NewsNotFoundError(date, file_name)

    return list_of_news


def retrieve_news_by_date(date, item_group, limit=None):
    """ Retrieve and return news by date from item group

    If limit is specified return limited count of news.

    :param date: date of news publishing
    :type date: 'datetime.datetime'

    :type item_group: 'items.ItemGroup'

    :param limit: limited count of returned news
    :type limit: int

    :rtype: 'items.ItemGroup'
    """
    items_by_date = list()

    for item in item_group.items:
        item_date = datetime.strptime(item.date.replace(',', ''), '%a %d %b %Y %H:%M:%S %z')

        if date.date() == item_date.date():
            items_by_date.append(item)

    if limit:
        items_by_date = items_by_date[:limit]

    return ItemGroup(feed=item_group.feed, items=items_by_date)


def retrieve_news_by_date_from_list(date, item_groups, limit=None):
    """ Retrieve and return news by date from list of item group

    If limit is specified return limited count of news.

    :param date: date of news publishing
    :type date: 'datetime.datetime'

    :type item_groups: list of 'items.ItemGroup'

    :param limit: limited count of returned news
    :type limit: int

    :rtype: list of 'items.ItemGroup'
    """
    item_groups_by_date = list()
    count = 0

    for item_gr in item_groups:
        if limit:
            left_to_add = limit - count
            if not left_to_add:
                break

            item_group_by_date = retrieve_news_by_date(date, item_gr, left_to_add)
            count += len(item_group_by_date.items)
        else:
            item_group_by_date = retrieve_news_by_date(date, item_gr)

        if item_group_by_date.items:
            item_groups_by_date.append(item_group_by_date)

    return item_groups_by_date
