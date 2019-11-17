from json import dumps as jdumps
from dataclasses import asdict


def news_as_json_str(item_group):
    """ Convert news in json format

    :type item_group: 'items.ItemGroup'
    :rtype: str
    """
    news_dict = asdict(item_group)

    return jdumps(news_dict, indent=4, ensure_ascii=False)


def news_as_json_str_from_list(item_groups):
    """ Convert list of news in json format

    :type item_groups: list of 'items.ItemGroup'
    :rtype: str
    """
    lst = [asdict(item_gr) for item_gr in item_groups]

    return jdumps(lst, indent=4, ensure_ascii=False)
