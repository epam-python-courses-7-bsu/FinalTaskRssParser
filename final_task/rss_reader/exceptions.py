""" Module for non-standard exceptions. """


class Error(Exception):
    """ Class to raising exceptions. """
    pass


class EmptyFileError(Error):
    pass


class EmptyCollectionError(Error):
    pass


class ComLineArgError(Error):
    pass


class FilePathError(Error):
    pass



