#!/usr/bin/env python3.8


class Error(Exception):
    """Base class for exceptions in this module"""


class InvalidURL(Error):
    """Exception is raised for invalid URL"""


class EmptyLink(Error):
    """Exception is raised for link without news"""
