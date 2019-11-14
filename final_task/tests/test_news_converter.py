import unittest
import news_converter
from items import Item


class TestNewsConverter(unittest.TestCase):
    def test_news_as_json_str(self):
        feed_title = 'feed title'
        items = [Item('title1', 'date1', 'link1', 'text1', ['src1', 'src2']),
                 Item('title2', 'date2', 'link2', 'text2', [])]

        extended_result = '{\n' + \
                          '    "feed": "feed title",\n' + \
                          '    "items": [\n' + \
                          '        {\n' + \
                          '            "title": "title1",\n' + \
                          '            "date": "date1",\n' + \
                          '            "link": "link1",\n' + \
                          '            "text": "text1",\n' + \
                          '            "img_links": [\n' + \
                          '                "src1",\n' + \
                          '                "src2"\n' + \
                          '            ]\n' + \
                          '        },\n' + \
                          '        {\n' + \
                          '            "title": "title2",\n' + \
                          '            "date": "date2",\n' + \
                          '            "link": "link2",\n' + \
                          '            "text": "text2",\n' + \
                          '            "img_links": []\n' + \
                          '        }\n' + \
                          '    ]\n' + \
                          '}'

        self.assertEqual(news_converter.news_as_json_str(feed_title, items), extended_result)
