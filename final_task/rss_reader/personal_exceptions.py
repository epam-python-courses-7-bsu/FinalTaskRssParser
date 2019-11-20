class IncorrectURL(Exception):
    def __str__(self) -> str:
        return 'The entered URL is incorrect'


class NoInternet(Exception):
    def __str__(self) -> str:
        return "Internet off, please check your connection"
