import unittest
import news_converter
from items import Item, ItemGroup


class TestNewsConverter(unittest.TestCase):
    def setUp(self):
        self.items = [Item('title1', 'date1', 'link1', 'text1', ['src1', 'src2']),
                      Item('title2', 'date2', 'link2', 'text2', [])]
        self.extended_items_list = '    "items": [\n' + \
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
                                   '    ]'

    def test_news_as_json_str(self):
        item_group = ItemGroup('feed title', self.items)

        extended_result = '{\n' + \
                          '    "feed": "feed title",\n' + \
                          self.extended_items_list + '\n' + \
                          '}'

        self.assertEqual(news_converter.news_as_json_str(item_group), extended_result)

    def test_news_as_json_str_from_list(self):
        item_group1 = ItemGroup('feed title 1', self.items)
        item_group2 = ItemGroup('feed title 2', self.items)

        extended_result = '[\n' + \
                          '    {\n' + \
                          '        "feed": "feed title 1",\n' + \
                          '    ' + self.extended_items_list.replace('\n', '\n    ') + '\n' + \
                          '    },\n' + \
                          '    {\n' + \
                          '        "feed": "feed title 2",\n' + \
                          '    ' + self.extended_items_list.replace('\n', '\n    ') + '\n' + \
                          '    }\n' + \
                          ']'

        item_groups = [item_group1, item_group2]
        self.assertEqual(news_converter.news_as_json_str_from_list(item_groups), extended_result)


if __name__ == '__main__':
    unittest.main()
