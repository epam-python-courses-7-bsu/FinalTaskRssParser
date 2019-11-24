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
        result['title'] = work_with_text.text_processing(data['feed']['title'])

        for item in data['entries']:
            temp = {
                'title': work_with_text.text_processing(item['title']),
                'published': work_with_text.text_processing(item['published']),
                'link': work_with_text.text_processing(item['link']),
                'summary': work_with_text.text_processing(item['summary'], links_on_image)
            }
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
