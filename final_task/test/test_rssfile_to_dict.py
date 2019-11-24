import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rss_reader'))

import work_with_feedparser
import work_with_dict


class TestRssToDict(unittest.TestCase):
    def test_rss_to_dict(self):
        data = work_with_feedparser.get_object_feed(os.path.abspath('test_rss.xml'))
        output = {
            'title': 'Head title',
            'items': [{
                'title': 'Title item1',
                'published': 'Thu, 1 Nov 2019 16:12:24 -0500',
                'link': 'link1',
                'summary': '[image: alt_text] des1',
                'contain_image': True,
                'link_on_image': 'link_img',
            },
                {
                    'title': 'Title item2',
                    'published': 'Thu, 2 Nov 2019 16:12:24 -0500',
                    'link': 'link2',
                    'summary': 'des2',
                    'contain_image': False,
                }
            ]
        }
        self.assertEqual(work_with_dict.to_dict(data), output)


if __name__ == '__main__':
    unittest.main()
