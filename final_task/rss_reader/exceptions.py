from datetime import datetime


class GettingRSSException(Exception):
    def __init__(self, msg):
        super().__init__('Problems with getting RSS: ' + msg)


class StorageNotFoundError(Exception):
    def __init__(self, storage_name):
        super().__init__('Storage ' + storage_name + ' not found.')


class NewsNotFoundError(Exception):
    def __init__(self, date, storage_name, source=None):
        date_string = datetime.strftime(date, '%Y.%m.%d')

        msg = 'News by date ' + date_string
        if source:
            msg += ' and by source ' + source

        super().__init__(msg + ' not found in storage ' + storage_name)
