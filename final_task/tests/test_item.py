import unittest
from item import Item


class TestItem(unittest.TestCase):
    def test_item_as_str(self):
        itm = Item('title', 'date', 'link', 'text', ['img1', 'img2'])
        expected_str = 'Title: title' \
                       '\nDate: date' \
                       '\nLink: link' \
                       '\nText: text' \
                       '\nImage links:' \
                       '\n\t[1]: [img1]' \
                       '\n\t[2]: [img2]\n'

        self.assertEqual(str(itm), expected_str)


if __name__ == '__main__':
    unittest.main()
