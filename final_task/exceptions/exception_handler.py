import feedparser


class ExceptionHandler(Exception):
    """Handles all exception that I provided"""

    def __init__(self, exc):
        self.exc = exc
