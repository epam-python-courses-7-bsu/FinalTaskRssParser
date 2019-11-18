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

    result = {'title': '', 'items': []}
    links_on_image = []
    if isinstance(data, FeedParserDict):
        for feed_element in structure['feed']:
            result[feed_element] = work_with_text.text_processing(data['feed'][feed_element])

        for item in data['entries']:
            temp = {}
            for items_element in structure['entries']:
                if items_element == 'summary':
                    temp[items_element] = work_with_text.text_processing(item[items_element], links_on_image)
                else:
                    temp[items_element] = work_with_text.text_processing(item[items_element])
            result['items'].append(temp)
        for index_link, link in enumerate(links_on_image):
            if link:
                result['items'][index_link]['contain_image'] = True
                result['items'][index_link]['link_on_image'] = links_on_image[index_link]
            else:
                result['items'][index_link]['contain_image'] = False
    return result


@decorators.functions_log
def limited_dict(data: dict, limit: int) -> dict:
    result = {
        'title': data['title'],
        'items': data['items'][:limit],
    }
    return result
