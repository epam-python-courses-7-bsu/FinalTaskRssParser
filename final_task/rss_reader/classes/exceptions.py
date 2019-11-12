"""Module contains custom exceptions"""


class InternetConnectionError(Exception):
    pass

class GettingFeedError(Exception):
    pass

class UrlError(Exception):
    pass

class LimitArgumentError(Exception):
    pass

class FeedXmlError(Exception):
    pass

class VersionPrinted(Exception):
    pass