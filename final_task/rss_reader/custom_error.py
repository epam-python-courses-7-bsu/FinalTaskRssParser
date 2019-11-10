class Error(Exception):
    """Base class for other exceptions"""


class UrlNotFoundInArgsError(Error):
    """Raised when can't find url in arguments"""
    pass


class NotEnoughArgumentsError(Error):
    """Raised when not enough arguments"""
    pass


class NotValidUrlError(Error):
    """Raised when url is not valid"""
    pass


class ConnectionFailedError(Error):
    """Raised when can't connect to the url"""
    message: str

    def __init__(self, message):
        if message:
            self.message = message


class ArticleKeyError(Error):
    """Raised when the article miss key"""
    message: str

    def __init__(self, message):
        if message:
            self.message = message
