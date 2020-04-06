import unittest
import news_converter
from item import Item
from item_group import ItemGroup


class TestNewsConverter(unittest.TestCase):
    def setUp(self):
        self.items_json = [Item('title1', 'date1', 'link1', 'text1', ['src1', 'src2']),
                           Item('title2', 'date2', 'link2', 'text2', [])]
        self.expected_json_str = '    "items": [\n' + \
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

        self.item1 = Item('title', 'date', 'link', 'before[image 1: alt1][1]middle[image 2: alt2][2]after',
                          ['img1', 'img2'])
        self.expected_html1 = 'before<p style="text-align: center;">' \
                              '<img src="img1" alt="alt1" style="margin-bottom: 30px;">' \
                              '</p>middle<p style="text-align: center;">' \
                              '<img src="img2" alt="alt2" style="margin-bottom: 30px;"></p>after'

        self.item2 = Item('title', 'date', 'link', 'text', [])
        self.expected_html2 = 'text'

        self.expected_items_html = '<div style="margin: 60px 15% 20px 15%;"><h3 align=center>title</h3>' \
                                   '<p align="justify">' + self.expected_html1 + '</p><br><small><i>' \
                                   '<a href=link color=blue>Go to source..</a><br>' \
                                   '<span style="float:right; margin-right:90">date</span></i></small><br></div>' \
                                   '<hr align=center size=1 width=70% color=black>' \
                                   '<div style="margin: 60px 15% 20px 15%;"><h3 align=center>title</h3>' \
                                   '<p align="justify">' + self.expected_html2 + '</p><br><small><i>' \
                                   '<a href=link color=blue>Go to source..</a><br>' \
                                   '<span style="float:right; margin-right:90">date</span></i></small><br></div>'

        self.item_gr = ItemGroup('feed', [self.item1, self.item2])

    def test_news_as_json_str(self):
        item_group = ItemGroup('feed title', self.items_json)

        expected_result = '{\n' + \
                          '    "feed": "feed title",\n' + \
                          self.expected_json_str + '\n' + \
                          '}'

        self.assertEqual(news_converter.news_as_json_str(item_group), expected_result)

    def test_news_as_json_str_from_list(self):
        item_group1 = ItemGroup('feed title 1', self.items_json)
        item_group2 = ItemGroup('feed title 2', self.items_json)

        expected_result = '[\n' + \
                          '    {\n' + \
                          '        "feed": "feed title 1",\n' + \
                          '    ' + self.expected_json_str.replace('\n', '\n    ') + '\n' + \
                          '    },\n' + \
                          '    {\n' + \
                          '        "feed": "feed title 2",\n' + \
                          '    ' + self.expected_json_str.replace('\n', '\n    ') + '\n' + \
                          '    }\n' + \
                          ']'

        item_groups = [item_group1, item_group2]
        self.assertEqual(news_converter.news_as_json_str_from_list(item_groups), expected_result)

    def test_item_text_with_imgs2html(self):
        resulting_str1 = news_converter.item_text_with_imgs2html(self.item1.text, self.item1.img_links)
        self.assertEqual(resulting_str1, self.expected_html1)

        resulting_str2 = news_converter.item_text_with_imgs2html(self.item2.text, self.item2.img_links)
        self.assertEqual(resulting_str2, self.expected_html2)

    def test_items2html(self):
        resulting_str = news_converter.items2html([self.item1, self.item2])
        self.assertEqual(resulting_str, self.expected_items_html)

    def test_news2html(self):
        item_groups = [ItemGroup('feed1', [self.item1, self.item2]), ItemGroup('feed2', [self.item1])]
        expected_str = '<html><head><title>News</title>' \
                       '<meta content="text/html; charset=utf-8" http-equiv="Content-Type"><style>' \
                       '@font-face {font-family: DejaVuSans;src: url("../fonts/DejaVuSansCondensed.ttf");}' \
                       'body {font-family: DejaVuSans;}</style></head><body><div>' \
                       '<hr align=center size=3 width=70% color=green><h1 align=center>feed1</h1>' \
                       '<hr align=center size=3 width=70% color=green><div>' + self.expected_items_html + \
                       '</div></div><div><hr align=center size=3 width=70% color=green><h1 align=center>feed2</h1>' \
                       '<hr align=center size=3 width=70% color=green><div><div style="margin: 60px 15% 20px 15%;">' \
                       '<h3 align=center>title</h3><p align="justify">' + self.expected_html1 + '</p><br><small><i>' \
                       '<a href=link color=blue>Go to source..</a><br><span style="float:right; margin-right:90">' \
                       'date</span></i></small><br></div></div></div></body></html>'

        resulting_str = news_converter.news2html(item_groups)
        self.assertEqual(resulting_str, expected_str)


if __name__ == '__main__':
    unittest.main()
