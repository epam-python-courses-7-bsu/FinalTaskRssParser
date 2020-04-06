import logging
from copy import deepcopy


colorize = False


def merge_lists(list1, list2):
    """ Merge two lists """
    logging.info('Merging lists')
    res_list = deepcopy(list1)

    for element in list2:
        if element not in res_list:
            res_list.append(element)

    return res_list
