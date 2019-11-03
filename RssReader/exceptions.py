"""This module provides the list of user exceptions"""


class WrongURLException(Exception):
    """The user type a wrong address"""
    pass


class EmptyRSSList(Exception):
    """The server does not respond"""
    pass
