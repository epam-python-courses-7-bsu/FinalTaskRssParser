#!/usr/bin/env python3.8


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class InvalidURL(Error):
    """Exception is raised for invalid URL"""
    pass


class FeedError(Error):
    """Exception is raised for link without news"""
    pass


class InvalidDateFormat(Error):
    """Exception is raised for date not in %%Y%%m%%d format"""
    pass


class SpecifiedDayNewsError(Error):
    """Exception is raised if on the specified day there are no entries in DB."""
    pass


class PATHError(Error):
    """Exception is raised if the wrong PATH was specified."""
    pass


class EmptyCacheError(Error):
    """Exception is raised if retrieving data from empty cache."""
    pass
