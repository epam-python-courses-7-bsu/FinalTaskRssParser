class RssReaderException(Exception):
    def __init__(self, message):
        self.expression = 'RssReaderException: '
        self.message = message


class FileException(RssReaderException):
    def __init__(self, message):
        self.expression = 'RssReaderException.FileException: '
        self.message = message


class ConnectException(RssReaderException):
    def __init__(self, message):
        self.expression = 'RssReaderException.ConnectException: '
        self.message = message