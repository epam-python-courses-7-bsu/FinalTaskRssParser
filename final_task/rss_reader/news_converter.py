import logging
import json
from dataclasses import asdict


def news_as_json_str(feed_title, items_):
    """ Convert news in json format

    :type feed_title: str
    :type items_: list of 'items.Item'
    :rtype: str
    """
    logging.info('Converting items to dicts.')
    map_of_dict_items = map(lambda item: asdict(item), items_)

    json_structure = {"feed": feed_title, "items": list(map_of_dict_items)}

    return json.dumps(json_structure, indent=4)
