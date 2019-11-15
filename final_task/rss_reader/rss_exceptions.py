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
