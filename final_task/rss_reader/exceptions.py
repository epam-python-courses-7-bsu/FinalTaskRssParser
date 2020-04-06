from datetime import datetime


class GettingRSSException(Exception):
    pass


class StorageNotFoundError(Exception):
    pass


class NewsNotFoundError(Exception):
    def __init__(self, date, storage_name, source=None):
        date_string = datetime.strftime(date, '%Y.%m.%d')

        msg = 'News by date ' + date_string
        if source:
            msg += ' and by source ' + source

        super().__init__(msg + ' not found in storage ' + storage_name)
