class Error(Exception):
    """Base class for other exceptions"""
    message: str

    def __init__(self, message):
        self.message = message


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
    pass


class ArticleKeyError(Error):
    """Raised when the article miss key"""
    pass
