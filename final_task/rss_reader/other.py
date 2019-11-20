"""This module contain various help functions"""

import sys


def choice() -> list:
    """Help the user to make choice"""

    user_choice = input().split()
    if user_choice[0] == 'q':
        sys.exit()
    else:
        return user_choice


date = 'Sun, 17 Nov 2019 06:00:35 -0500'


def convert_date(date: str):
    """This function converts date"""
    month = {'Jan': '1',
             'Feb': '2',
             'Mar': '3',
             'Apr': '4',
             'May': '5',
             'Jun': '6',
             'Jul': '7',
             'Aug': '8',
             'Sep': '9',
             'Oct': '10',
             'Nov': '11',
             'Dec': '12'}
    day = date[5:7]
    month_num = month[date[8:11]]
    year = date[12:16]

    return year+month_num+day
