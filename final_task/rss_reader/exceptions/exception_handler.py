import feedparser


class ContentTypeException(Exception):
    # raise feedparser.NonXMLContentType
    pass

class LimitException(Exception):
    pass


