class IncorrectURL(Exception):
    def __str__(self) -> str:
        return 'The entered URL is incorrect'


class NoInternet(Exception):
    def __str__(self) -> str:
        return "Internet off, please check your connection"

class IncorrectFilePath(Exception):
    def __init__(self, message):
        self.message=message

    def __str__(self) -> str:
        return self.message