import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rss_reader'))
import work_with_dict


class TestDictFunctions(unittest.TestCase):
    def test_limited_dict(self):
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
            ]
        }
        output = {
            'title': 'titl',
            'items': [{
                'title': 't1',
                'published': 'date1',
                'link': 'link1',
                'summary': 'des1',
            }]
        }
        self.assertEqual(work_with_dict.limited_dict(entering_dict, 1), output)
        self.assertEqual(work_with_dict.limited_dict(entering_dict, 2), entering_dict)


if __name__ == '__main__':
    unittest.main()
