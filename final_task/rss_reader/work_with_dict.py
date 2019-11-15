import json
from feedparser import FeedParserDict
import decorators
import work_with_text


@decorators.functions_log
def to_dict(data) -> dict:
    """convert data to JSON format"""

    structure = {
        'feed': [
            'title'
        ],
        'entries': [
            'title',
            'published',
            'link',
            'summary'
        ]
    }

    result = {'title': '', 'items': [], 'links': []}
    if isinstance(data, FeedParserDict):
        for feed_element in structure['feed']:
            result[feed_element] = work_with_text.text_processing(data['feed'][feed_element], result['links'])

        for item in data['entries']:
            temp = {}
            for items_element in structure['entries']:
                temp[items_element] = work_with_text.text_processing(item[items_element], result['links'])
            result['items'].append(temp)
    elif isinstance(data, str):
        result['error'] = data
    return result


@decorators.functions_log
def limited_dict(data: dict, limit: int) -> dict:
    result = {}
    if isinstance(data, dict):
        result['title'] = data['title']
        result['items'] = data['items'][:limit]
        result['links'] = data['links'][:limit]
    else:
        result['error'] = data
    return result
