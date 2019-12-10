import unittest
from output_functions import printing_title


class MyTestCase(unittest.TestCase):
    def test_if_string(self):
        feed = {'feed': {'title': 'Yahoo News - Latest News & Headlines', 'entries': [{}, {}, {}]}}
        self.assertEqual(printing_title(feed), 'Yahoo News - Latest News & Headlines', "Should be Yahoo News...")

    def test_if_not_string(self):
        feed = {'feed': {'title': 55, 'entries': [{}, {}, {}]}}
        self.assertEqual(printing_title(feed), 55, "Should be 55")

    def test_if_none(self):
        feed = {'feed': {'title': None, 'entries': [{}, {}, {}]}}
        self.assertEqual(printing_title(feed), None, "Should be None")

    def test_if_no_title(self):
        feed = {'feed': {'entries': [{}, {}, {}]}}
        self.assertNotEqual(printing_title(feed), 'Yahoo News - Latest News & Headlines', "Should be None")


if __name__ == '__main__':
    unittest.main()
