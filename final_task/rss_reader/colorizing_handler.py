"""Module to setup colorize"""
import colorama

COLORIZING_STATUS = False
colorama.init()


def set_colorizing_status() -> None:
    """Sets COLORIZING_STATUS to true"""
    global COLORIZING_STATUS
    COLORIZING_STATUS = True


def reset_colorizing_status() -> None:
    """Resets COLORIZING_STATUS to false"""
    global COLORIZING_STATUS
    COLORIZING_STATUS = False
