import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rss_reader'))
import work_with_html


class TestHtmlFunctions(unittest.TestCase):
    def test_something(self):
        entering_dict = {
            'title': 'titl',
            'items': [{
                    'title': 't1',
                    'published': 'date1',
                    'link': 'link1',
                    'summary': 'des1',
                    'contain_image': False,

                },
                {
                    'title': 't2',
                    'published': 'date2',
                    'link': 'link2',
                    'summary': '[image: alt]des2',
                    'contain_image': True,
                    'link_on_image': 'imgLink',
                }
            ]
        }
        output = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>titl</title><style type="text/css">' + \
                 'body{text-align: center; font-size: 120%;font-family: Verdana, Arial, Helvetica, sans-serif;' + \
                 'color: #333366; } </style></head><center><h1>titl</h1></center><br><h3><center><a href="link1">' + \
                 't1</a></center></h3>date1<br>des1<br><br><h3><center><a href="link2">t2</a></center></h3>date2<br>' +\
                 '<img src="imgLink" alt=" alt"><br>des2<br><br>'
        self.assertEqual(work_with_html.text_processing_for_html(entering_dict), output)


if __name__ == '__main__':
    unittest.main()
