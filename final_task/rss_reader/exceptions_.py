class FeedError(Exception):
    '''
    Raise when something is wrong with feed
    '''
    pass


class InvalidArgs(FeedError):
    pass


class ConvertionError(FeedError):
    pass
