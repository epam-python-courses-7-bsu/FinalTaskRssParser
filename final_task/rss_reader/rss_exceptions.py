#!/usr/bin/env python3.8


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class LimitSignError(Error):
    """Exception is raised negative limit value"""
    pass


class FeedError(Error):
    """Exception is raised for link without news"""
    pass


class InternetConnectionError(Error):
    """Exception is raised if no Internet connection."""
    pass


class UnreachableURLError(Error):
    """Exception is raised if URL is unreachable"""
    pass


class URLResponseError(Error):
    """Exception occurs while retrieving status code from the URL other than 200"""
    pass


class FormatDateError(Error):
    """Exception is raised if date was setted in invalid format"""
    pass


class SpecifiedDayNewsError(Error):
    """Exception is raised if on the specified day there are no entries in DB."""
    pass


class EmptyCacheError(Error):
    """Exception is raised if retrieving data from empty cache."""
    pass


class PATHError(Error):
    """Exception is raised if the wrong PATH was specified."""
    pass
