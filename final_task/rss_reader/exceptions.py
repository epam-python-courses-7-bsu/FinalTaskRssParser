""" Module for non-standard exceptions. """


class Error(Exception):
    """ Class to raising exceptions. """
    def __init__(self, message):
        super().__init__(message)



