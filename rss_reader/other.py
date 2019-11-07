"""This module contain various help functions"""

import sys


def choice() -> list:
    """Help the user to make choice"""

    user_choice = input().split()
    if user_choice[0] == 'q':
        sys.exit()
    else:
        return user_choice


