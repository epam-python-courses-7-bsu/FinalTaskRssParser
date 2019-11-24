"""Module to setup colorize"""
import colorama

COLORIZING_STATUS = False
colorama.init()


def set_colorizing_status() -> None:
    """Sets COLORIZING_STATUS to true if --colorize in arguments"""
    global COLORIZING_STATUS
    COLORIZING_STATUS = True
