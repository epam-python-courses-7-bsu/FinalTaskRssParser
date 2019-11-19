import colorama

COLORIZING_STATUS = False


def set_colorizing_status() -> None:
    """Sets COLORIZING_STATUS to true if --colorize in arguments"""
    colorama.init()
    global COLORIZING_STATUS
    COLORIZING_STATUS = True
