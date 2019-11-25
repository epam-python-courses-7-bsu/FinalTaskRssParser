"""
RSS reader exception classes
"""


class CacheNotFoundError(Exception):
    """Articles for the requested date or url does not exist"""
    pass


class NoDataToConvertError(Exception):
    """There is no data to convert"""
    pass


class GoForRssError(Exception):
    """Website is not working or Url is not correct. Please, try again"""
    pass


class WrongResponseTypeError(Exception):
    """Cannot find any rss feed for this URL"""
    pass
