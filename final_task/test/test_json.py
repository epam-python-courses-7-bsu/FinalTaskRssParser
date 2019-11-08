import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rss_reader'))
import work_with_json


class TestJsonFunctions(unittest.TestCase):
    def test_limited_json(self):
        entering_dict = {
            'title': 'titl',
            'items': [{
                'title': 't1',
                'published': 'date1',
                'link': 'link1',
                'summary': 'des1',
            },
                {
                    'title': 't2',
                    'published': 'date2',
                    'link': 'link2',
                    'summary': 'des2'
                }
            ],
            'links': [
                'first',
                'second'
            ]
        }
        output = {
            'title': 'titl',
            'items': [{
                'title': 't1',
                'published': 'date1',
                'link': 'link1',
                'summary': 'des1',
            }],
            'links': ['first']}
        self.assertEqual(work_with_json.limited_json(entering_dict, 1), output)
        self.assertEqual(work_with_json.limited_json(entering_dict, 2), entering_dict)


if __name__ == '__main__':
    unittest.main()
