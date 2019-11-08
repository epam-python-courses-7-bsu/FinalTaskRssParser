import json
from feedparser import FeedParserDict
from rss_reader.decorators import functions_log
from rss_reader.work_with_text import text_processing


@functions_log
def to_json(data) -> json:
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
            result[feed_element] = text_processing(data['feed'][feed_element], result['links'])

        for item in data['entries']:
            temp = {}
            for items_element in structure['entries']:
                temp[items_element] = text_processing(item[items_element], result['links'])
            result['items'].append(temp)
    elif isinstance(data, str):
        result['error'] = data
    result = json.dumps(result)
    return result


@functions_log
def limited_json(data: dict, limit: int) -> dict:
    result = {}
    if isinstance(data, dict):
        result['title'] = data['title']
        result['items'] = data['items'][:limit]
        result['links'] = data['links'][:limit]
    else:
        result['error'] = data
    return result
